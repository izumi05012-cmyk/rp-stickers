"""Normalize a newly authored soft chibi sticker; retain smooth transparent edges."""
from pathlib import Path
from PIL import Image
import numpy as np,json,sys,hashlib,shutil
source=Path(sys.argv[1]);name=sys.argv[2];title=sys.argv[3];number=int(sys.argv[4]);assert name.startswith('ws_') and '/' not in name
im=Image.open(source).convert('RGBA');original_size=im.size;a=np.array(im);ys,xs=np.nonzero(a[:,:,3]>8);assert len(xs)>100
im=im.crop((int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)))
scale=min(468/im.width,468/im.height);size=(round(im.width*scale),round(im.height*scale));im=im.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')
out=Image.new('RGBA',(512,512));out.paste(im,((512-im.width)//2,(512-im.height)//2));a=np.array(out);a[a[:,:,3]<=2]=0;out=Image.fromarray(a)
assert a[:,:,3].min()==0 and a[:,:,3].max()>200;ys,xs=np.nonzero(a[:,:,3]);assert xs.min()>=20 and ys.min()>=20 and xs.max()<=491 and ys.max()<=491
p=Path('wangshu')/(name+'.png');out.save(p,optimize=True);shutil.copy2(p,Path('s')/p.name)
meta_path=Path('previews/ws-v2/manifest.json');meta=json.loads(meta_path.read_text()) if meta_path.exists() else {'batch':'ws-v2','canvas':[512,512],'style':'same soft hand-drawn Little Wangshu chibi as existing16','stickers':[]}
item={'number':number,'name':name,'title':title,'file':str(p),'flatFile':'s/'+p.name,'canvas':[512,512],'alphaBounds':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'sourceSize':list(original_size),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'resize':'proportional,premultiplied alpha,Lanczos,transparent padding'}
meta['stickers']=[v for v in meta['stickers'] if v['name']!=name]+[item];meta['stickers'].sort(key=lambda v:v['number']);meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
listing=Path('s/LIST.txt');text=listing.read_text();heading='## 来自 wangshu · 小望舒第二批（512×512）'
if heading not in text:text+='\n'+heading+'\n'
if p.name not in text.splitlines():text+=p.name+'\n'
listing.write_text(text)
print(json.dumps({'file':str(p),'size':[512,512],'bounds':item['alphaBounds'],'flatCopyIdentical':p.read_bytes()==(Path('s')/p.name).read_bytes()},ensure_ascii=False))
