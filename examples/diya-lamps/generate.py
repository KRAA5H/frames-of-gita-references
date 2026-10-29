#!/usr/bin/env python3
"""
Frames of Gita - example: diya lamps cascade (code-built animation).

Four terracotta oil lamps (diyas) on dark ground. The first flame passes
from lamp to lamp until all four burn, the scene slowly pulls out, and a
closing line appears: "from one flame, many lights". Every pixel is drawn
by this script with numpy and Pillow - no AI imagery, no third-party
assets. 13 seconds, 24 fps, 1080x1920.

Dependencies:
    Python 3.9+
    pip install pillow numpy
    ffmpeg on PATH

Run:
    python3 generate.py              renders all frames and writes diya-lamps.mp4
    python3 generate.py --test       writes 6 preview frames to ./preview/ only
"""

import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H = 1080,1920
FPS=24; DUR=13.0
WS=1.10
WW,WH=int(W*WS),int(H*WS)
OUT=None  # frames directory is chosen in main()

BG_TOP=(20,15,11); BG_BOT=(6,4,3)
TERRA_HI=(214,132,80); TERRA_D=(112,56,32); UMBER=(46,28,16)
OIL=(118,70,18); OIL_HI=(255,200,115)
AMBER=(255,176,66); ORANGE=(255,150,40); PALE=(255,240,205); EMBER=(255,110,30)
OFFWHITE=(245,238,224)
SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'

# lamps: (x_frac, y_frac, scale, ignition_time or None if lit from start)
LAMPS=[(0.26,0.55,1.4,None),(0.46,0.60,1.55,2.2),(0.66,0.57,1.45,4.4),(0.50,0.76,2.1,6.6)]
IGN_DUR=0.9

def np_to_img(a): return Image.fromarray(a.astype(np.uint8),'RGB')

def background():
    y=np.linspace(0,1,WH)[:,None]
    top=np.array(BG_TOP,float); bot=np.array(BG_BOT,float)
    col=top[None,None,:]*(1-y[:,:,None])+bot[None,None,:]*y[:,:,None]
    a=np.repeat(col,WW,axis=1)
    yy,xx=np.mgrid[0:WH,0:WW]
    r=np.sqrt(((xx-WW/2)/(WW*0.62))**2+((yy-WH*0.42)/(WH*0.62))**2)
    a*=np.clip(1.12-0.5*r**2,0,1)[:,:,None]
    return np_to_img(a)

def ground(img,horizon):
    d=ImageDraw.Draw(img,'RGBA')
    d.rectangle([0,horizon,WW,WH], fill=(24,16,10,255))
    rng=np.random.default_rng(7)
    for i in range(40):
        gy=horizon+8+(WH-horizon)*rng.random()
        x0=rng.random()*WW; ln=60+rng.random()*260
        v=int(18+26*rng.random())
        d.line([x0,gy,x0+ln,gy+(rng.random()-0.5)*6], fill=(v+22,v+8,v,70), width=2)

def glow_sprite(px=512):
    yy,xx=np.mgrid[0:px,0:px]
    r=np.sqrt((xx-px/2)**2+(yy-px/2)**2)/(px/2)
    fall=np.exp(-(r**2)*3.2)
    a=np.zeros((px,px,4),np.uint8)
    a[...,0]=255; a[...,1]=170; a[...,2]=70
    a[...,3]=(fall*255).astype(np.uint8)
    return Image.fromarray(a,'RGBA')
GLOW=glow_sprite()

def diya(cx,cy,s,lit=True):
    """Returns (layer, wick_tip)."""
    lay=Image.new('RGBA',(WW,WH),(0,0,0,0))
    bw,bh=300*s,132*s
    sh=Image.new('RGBA',(WW,WH),(0,0,0,0))
    ImageDraw.Draw(sh).ellipse([cx-bw*0.62,cy+bh*0.20,cx+bw*0.62,cy+bh*0.80], fill=(0,0,0,150))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9*s)))
    grad=np.zeros((int(bh),int(bw),4),np.uint8)
    for j in range(int(bh)):
        u=j/int(bh)
        c=np.array(TERRA_HI)*(1-u)+np.array(TERRA_D)*u
        xs=np.linspace(0,1,int(bw))
        shade=0.82+0.36*(1-xs)*(0.6+0.4*(1-u))
        grad[j,:,0:3]=(c[None,:]*shade[:,None]).astype(np.uint8)
        grad[j,:,3]=255
    g=Image.fromarray(grad,'RGBA')
    mask=Image.new('L',(int(bw),int(bh)),0)
    ImageDraw.Draw(mask).ellipse([0,0,int(bw),int(bh)],fill=255)
    body=Image.new('RGBA',(int(bw),int(bh)),(0,0,0,0))
    body.paste(g,(0,0),mask)
    if not lit:
        body=body.point(lambda v:int(v*0.45))
    lay.alpha_composite(body,(int(cx-bw/2),int(cy-bh/2)))
    d=ImageDraw.Draw(lay,'RGBA')
    rw,rh=bw*0.86,bh*0.52
    d.ellipse([cx-rw/2,cy-rh/2-bh*0.10,cx+rw/2,cy+rh/2-bh*0.10], fill=UMBER+(255,))
    if lit:
        d.arc([cx-rw/2,cy-rh/2-bh*0.10,cx+rw/2,cy+rh/2-bh*0.10],160,380,fill=TERRA_HI+(220,),width=int(5*s/2.3))
    ow,oh=rw*0.82,rh*0.66
    oc=(cx,cy-bh*0.10)
    d.ellipse([oc[0]-ow/2,oc[1]-oh/2,oc[0]+ow/2,oc[1]+oh/2], fill=OIL+(255,))
    wx=oc[0]+ow*0.12
    wlen=34*s
    wtip=(wx+5*s, oc[1]-wlen)
    d.line([wx,oc[1],wtip[0],wtip[1]], fill=(28,18,12,255), width=int(8*s/2.3*2))
    return lay, wtip

def flame_poly(lx,ly,h,w,lean):
    def td(ht,wf,ln):
        tip=(lx+ln,ly-h*ht); lc=(lx-w*wf,ly-h*ht*0.42); rc=(lx+w*wf,ly-h*ht*0.42)
        bl=(lx-w*wf*0.52,ly); br=(lx+w*wf*0.52,ly)
        pts=[]; n=24
        for i in range(n+1):
            u=i/n
            pts.append(((1-u)**2*bl[0]+2*(1-u)*u*lc[0]+u**2*tip[0],(1-u)**2*bl[1]+2*(1-u)*u*lc[1]+u**2*tip[1]))
        for i in range(n+1):
            u=i/n
            pts.append(((1-u)**2*tip[0]+2*(1-u)*u*rc[0]+u**2*br[0],(1-u)**2*tip[1]+2*(1-u)*u*rc[1]+u**2*br[1]))
        return pts
    return td

def draw_flame(layer,t,x,y,size,scale=1.0):
    size=size*scale
    if size<2: return
    h=size*(1+0.07*math.sin(t*13)+0.045*math.sin(t*7.3+1.2))
    w=size*0.52*(1+0.05*math.sin(t*11.1+2.1))
    lean=size*0.10*(math.sin(t*5.1)+0.5*math.sin(t*9.7+0.6))
    pad=int(size*1.2)
    x0=max(0,int(x-w*2-pad)); y0=max(0,int(y-h*1.3-pad))
    x1=min(layer.size[0],int(x+w*2+pad+abs(lean)+8)); y1=min(layer.size[1],int(y+pad))
    fl=Image.new('RGBA',(x1-x0,y1-y0),(0,0,0,0))
    lx,ly=x-x0,y-y0
    d=ImageDraw.Draw(fl)
    td=flame_poly(lx,ly,h,w,lean)
    d.polygon(td(1.12,1.35,lean*1.2), fill=(255,120,25,90))
    d.polygon(td(1.0,1.0,lean), fill=ORANGE+(235,))
    d.polygon(td(0.74,0.62,lean*0.8), fill=AMBER+(240,))
    d.polygon(td(0.46,0.34,lean*0.6), fill=PALE+(255,))
    fl=fl.filter(ImageFilter.GaussianBlur(max(1.2,size*0.018)))
    layer.alpha_composite(fl,(x0,y0))
    gs=int(size*4.8*(1+0.06*math.sin(t*6.3)))
    g=GLOW.resize((gs,gs))
    g.putalpha(g.getchannel('A').point(lambda a:int(a*0.30)))
    layer.alpha_composite(g,(int(x-gs/2),int(y-h*0.45-gs/2)))

def flame_bridge(layer,t,p1,p2,u):
    """Flame tongue stretching from p1 (lit flame base) to p2 (new wick tip), u in [0,1]."""
    reach=p1[0]+(p2[0]-p1[0])*u, p1[1]+(p2[1]-p1[1])*u
    mid=((p1[0]+reach[0])/2, min(p1[1],reach[1])-60-30*math.sin(t*9))
    d=ImageDraw.Draw(layer)
    pts_top=[]; pts_bot=[]; n=20
    for i in range(n+1):
        v=i/n
        bx=(1-v)**2*p1[0]+2*(1-v)*v*mid[0]+v**2*reach[0]
        by=(1-v)**2*p1[1]+2*(1-v)*v*mid[1]+v**2*reach[1]
        wd=14*(1-v)+4*v
        pts_top.append((bx,by-wd)); pts_bot.append((bx,by+wd*0.6))
    d.polygon(pts_top+pts_bot[::-1], fill=(255,160,60,200))
    inner_top=[(x,y-w*0.5) for x,y,w in [(p[0],p[1]+ (14*(1-i/n)+4*(i/n))*0.2, 14*(1-i/n)+4*(i/n)) for i,p in enumerate(pts_top)]]
    d.polygon([(x,y) for x,y in inner_top]+pts_bot[::-1], fill=(255,220,150,220))

def light_env(t):
    L=0.30
    for (_,_,_,ig) in LAMPS:
        if ig is not None:
            L+=0.20*min(1,max(0,(t-ig)/0.6))
    return min(1.0,L)

def text_card():
    card=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(card)
    f=ImageFont.truetype(SERIF,88)
    for j,(txt,col) in enumerate([('from one flame,',OFFWHITE),('many lights',AMBER)]):
        wdt=sum(d.textlength(c,font=f) for c in txt)+5*(len(txt)-1)
        x=(W-wdt)/2
        for c in txt:
            w=d.textlength(c,font=f)
            d.text((x+3,300+j*120+4),c,font=f,fill=(0,0,0,180))
            d.text((x,300+j*120),c,font=f,fill=col)
            x+=w+5
    return card
CARD=text_card()

def build_world():
    base=background().convert('RGBA')
    ground(base,WH*0.60)
    items=[]
    for xf,yf,s,ig in LAMPS:
        lay,tip=diya(WW*xf,WH*yf,s,lit=(ig is None))
        base.alpha_composite(lay)
        items.append((WW*xf,WH*yf,s,ig,tip))
    return base,items

def render_frame(t,base,items):
    L=light_env(t)
    z=1.0+0.10*(t/DUR)   # slow pull-out
    cw,ch=W/z,H/z
    cx0=(WW-cw)/2; cy0=(WH-ch)/2
    frame=base.copy()
    # global wash grows with L
    wash_r=int((0.3+0.7*L)*WW*0.8)
    wash=GLOW.resize((wash_r,wash_r))
    wash.putalpha(wash.getchannel('A').point(lambda a:int(a*0.18*L)))
    frame.alpha_composite(wash,(int(WW*0.5-wash_r/2),int(WH*0.58-wash_r/2)))
    frame=frame.crop((int(cx0),int(cy0),int(cx0+cw),int(cy0+ch))).resize((W,H),Image.LANCZOS).convert('RGBA')
    sc=W/cw
    def M(p): return ((p[0]-cx0)*sc,(p[1]-cy0)*sc)
    # ground pools + flames per lamp state
    for idx,(xf,yf,s,ig,tip) in enumerate(items):
        phase=t+idx*1.7
        lit_t = 0 if ig is None else ig+IGN_DUR*0.55
        grown = 1 if ig is None else min(1,max(0,(t-(ig+IGN_DUR*0.5))/0.5))
        mp=M((xf,yf))
        # ground pool
        if grown>0:
            pool=Image.new('RGBA',(W,H),(0,0,0,0))
            ImageDraw.Draw(pool).ellipse([mp[0]-150*s*sc*0.5,mp[1]+20*s*sc,mp[0]+150*s*sc*0.5,mp[1]+95*s*sc], fill=(255,150,60,int(50*grown)))
            frame.alpha_composite(pool.filter(ImageFilter.GaussianBlur(14)))
        # ember during ignition contact
        if ig is not None and ig+IGN_DUR*0.4<t<ig+IGN_DUR*0.7:
            et=M(tip); er=(4+2*math.sin(t*9))*sc
            ImageDraw.Draw(frame).ellipse([et[0]-er,et[1]-er,et[0]+er,et[1]+er], fill=EMBER+(220,))
        # flame
        if t>=lit_t or ig is None:
            flare=1.0
            if ig is not None and t<ig+IGN_DUR+0.4:
                flare=1.0+0.9*max(0,1-(t-(ig+IGN_DUR*0.55))/0.5)
            ft=M(tip)
            draw_flame(frame,phase,ft[0],ft[1],95*s/2.3*sc,scale=grown*flare)
        # ignition bridge from previous lamp
        if ig is not None and ig<=t<ig+IGN_DUR*0.6:
            prev=items[idx-1]
            p1=M((prev[4][0],prev[4][1]-95*prev[2]/2.3*0.9))
            p2=M(tip)
            u=min(1,(t-ig)/(IGN_DUR*0.55))
            flame_bridge(frame,t,p1,p2,u)
    # closing text
    if 10.5<=t:
        a=1.0
        if t<11.2: a=(t-10.5)/0.7
        cc=CARD.copy()
        cc.putalpha(cc.getchannel('A').point(lambda v:int(v*a)))
        frame.alpha_composite(cc)
    return frame.convert('RGB')

def main():
    import shutil, subprocess, sys, tempfile
    base, items = build_world()
    if '--test' in sys.argv:
        out = os.path.join(os.getcwd(), 'preview')
        os.makedirs(out, exist_ok=True)
        for t in [1.0, 2.9, 5.2, 7.3, 9.5, 12.5]:
            render_frame(t, base, items).save(f'{out}/t{int(t*10):03d}.png')
        print('preview frames written to', out)
        return
    total = int(DUR * FPS)
    tmp = tempfile.mkdtemp(prefix='diya-')
    try:
        for k in range(total):
            render_frame(k / FPS, base, items).save(f'{tmp}/f{k:04d}.png')
            if k % FPS == 0:
                print(f'rendered second {k // FPS + 1}/{int(DUR)}', flush=True)
        out_mp4 = 'diya-lamps.mp4'
        cmd = ['ffmpeg', '-y', '-framerate', str(FPS), '-i', f'{tmp}/f%04d.png',
               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', out_mp4]
        print('encoding:', ' '.join(cmd))
        subprocess.run(cmd, check=True)
        print(f'done: {out_mp4} ({os.path.getsize(out_mp4)} bytes)')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
