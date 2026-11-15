from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,zipfile,hashlib,re
root=Path('.');outdir=Path('previews/ws-v2');meta=json.loads((outdir/'manifest.json').read_text());items=meta['stickers'];assert [v['number'] for v in items]==list(range(1,11));checks=[];hashes=set()
for v in items:
 p=Path(v['file']);im=Image.open(p);assert im.mode=='RGBA' and im.size==(512,512);a=np.array(im);assert a[:,:,3].min()==0 and a[:,:,3].max()>200;assert ((a[:,:,3]>0)&(a[:,:,3]<255)).any();ys,xs=np.nonzero(a[:,:,3]);assert xs.min()>=20 and ys.min()>=20 and xs.max()<=491 and ys.max()<=491;assert p.read_bytes()==Path(v['flatFile']).read_bytes();digest=hashlib.sha256(p.read_bytes()).hexdigest();hashes.add(digest);checks.append({'name':v['name'],'canvas':[512,512],'transparent':True,'softAlphaRetained':True,'flatCopyIdentical':True,'sha256':digest})
assert len(hashes)==10
fontfile='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';font=ImageFont.truetype(fontfile,21);small=ImageFont.truetype(fontfile,12);title=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',30)
board=Image.new('RGB',(1152,1064),'#211d22');d=ImageDraw.Draw(board);d.text((20,10),'小望舒 · 第二批 10 张',font=title,fill='#f5e6d1');d.text((20,50),'512×512 透明 PNG · 原来的柔和手绘 Q 版',font=font,fill='#debcaa')
for i,v in enumerate(items):
 x=16+i%4*284;y=92+i//4*322;d.rounded_rectangle((x,y,x+270,y+310),radius=12,fill='#30282a',outline='#73594b',width=2);im=Image.open(v['file']).convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');board.paste(im,(x+7,y+4),im);d.text((x+10,y+259),f"{v['number']}. {v['title']}",font=font,fill='#f5e6d1');d.text((x+10,y+289),v['name'],font=small,fill='#debcaa')
board.save(outdir/'overview.png')
cards=''.join(f'<article><a href="../../{v["file"]}" download><img loading="lazy" src="../../{v["file"]}" alt="{v["title"]}"></a><h3>{v["number"]}. {v["title"]}</h3><code>{v["name"]}.png</code><p><a href="../../{v["file"]}" download>下载 PNG</a></p></article>' for v in items)
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>小望舒 · 第二批表情包</title><style>
*{box-sizing:border-box}body{margin:0;background:#211d22;color:#f5e6d1;font:16px/1.6 system-ui}main{max-width:1160px;margin:auto;padding:20px}h1{font-size:28px}a{color:#edbea6}button{font:inherit;padding:9px 12px;border:1px solid #ac8772;border-radius:8px;margin:4px;background:#30282a;color:#f5e6d1;cursor:pointer}button[aria-pressed=true]{background:#765746}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}article{padding:12px;border:1px solid #73594b;border-radius:12px;background:#30282a;overflow:hidden}article>a{display:block;background:repeating-conic-gradient(#30282a 0% 25%,#3e3436 0% 50%) 0/16px 16px}article img{display:block;width:100%;height:auto;aspect-ratio:1;object-fit:contain}h3{font-size:18px;margin:12px 0 0}code{font-size:12px;overflow-wrap:anywhere}p{margin:8px 0}body.light article>a{background:#f5e6d1}body.dark article>a{background:#171417}footer{margin:28px 0;font-size:14px}@media(max-width:360px){main{padding:12px}.grid{grid-template-columns:1fr}}
</style><main><h1>小望舒 · 第二批表情包</h1><p>十张新表情，512×512 透明底，沿用原来的橘发狐耳与奶白开衫。</p><nav><button data-bg="" aria-pressed="true">棋盘底</button><button data-bg="light" aria-pressed="false">浅底</button><button data-bg="dark" aria-pressed="false">深底</button></nav><p><a href="overview.png">查看整批总览</a></p><div class="grid">CARDS</div><footer>点击图片或下载 PNG 即可取原图。背景颜色仅供查看透明边缘。</footer></main><script>
for(const button of document.querySelectorAll('[data-bg]'))button.onclick=()=>{document.body.classList.remove('light','dark');if(button.dataset.bg)document.body.classList.add(button.dataset.bg);for(const b of document.querySelectorAll('[data-bg]'))b.setAttribute('aria-pressed',String(b===button))};
</script></html>'''.replace('CARDS',cards)
(outdir/'index.html').write_text(page)
for url in re.findall(r'(?:src|href)="([^"]+)"',page):assert (outdir/url).exists(),url
report={'stickers':10,'canvas':[512,512],'allTransparent':True,'softAlphaRetained':True,'allMarginsAtLeast20px':True,'uniqueImages':10,'flatCopiesIdentical':True,'visualReview':['yes/no text and torn halves','two cheek handprints and teary smile','drooping ears and tail hug','hands on hips and high tail','apron and OK gesture','pinky corrected,thumb folded','face buried in fox plush','blue ski suit and goggles','single exclamation mark','one smoke wisp over desk'],'files':checks};(outdir/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
batch_readme='''# 小望舒 · 第二批 10 张

本批为柔和手绘 Q 版，不是像素游戏精灵。橘发狐耳、奶白开衫、大尾巴、琥珀眼与银饰红坠延续旧 16 张；第 5 张增加店员围裙，第 8 张按要求穿蓝色雪服与雪镜。

每张独立 RGBA PNG、512×512，保留柔和透明边缘并留出至少 20px 空白。图上只有第 1 张的 yes / 撕开的 no 和第 9 张的 ! 属于要求的文字/符号，其他小装饰为原系列风格。第 6 张已修正手型：小拇指上缠红绳，拇指收在掌心。

仓库内新图在 wangshu/ 和 s/ 各放一份，内容完全一致；本批按张生成、检查和推送。原有 16 张没有修改。

本页 index.html 可切换深浅背景看透明边缘。overview.png 是总览，不作为透明表情原图。verification.json 登记尺寸、透明、留白、双目录一致性和人工检查项。

下载压缩包时只收一份十张表情，避免重复；打开 preview.html 查看，直接使用 ws_ 开头的 PNG。新图目前在 codex/ws-stickers-v2 分支，尚未合并主分支。
''';(outdir/'README.md').write_text(batch_readme)
readme=Path('README.md');text=readme.read_text();start='<!-- ws-v2:start -->';end='<!-- ws-v2:end -->';section='\n'+start+'\n## wangshu/ 小望舒第二批（10 张，512×512）\n\n验收分支：`codex/ws-stickers-v2`。新图在 `wangshu/` 与 `s/` 各有相同一份，旧 16 张保持原样。\n\n[整批总览](previews/ws-v2/overview.png) · [透明底预览页](previews/ws-v2/index.html)\n\n| 文件 | 表情 |\n| --- | --- |\n'+''.join(f"| [{v['name']}.png]({v['file']}) | {v['title']} |\n" for v in items)+end+'\n'
if start in text:text=text[:text.index(start)]+text[text.index(end)+len(end):]
readme.write_text(text.rstrip()+'\n'+section)
zipname=Path('/workspace/sprite-materials/rp-stickers-wangshu-v2.zip')
with zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED) as z:
 for v in items:z.write(v['file'],'wangshu-v2/'+Path(v['file']).name)
 z.write(outdir/'overview.png','wangshu-v2/overview.png');z.writestr('wangshu-v2/preview.html',page.replace('../../wangshu/',''));z.writestr('wangshu-v2/README.md',batch_readme.replace('本页 index.html','preview.html'))
 zipmeta={**meta,'stickers':[{**{k:val for k,val in v.items() if k!='flatFile'},'file':Path(v['file']).name} for v in items]};z.writestr('wangshu-v2/manifest.json',json.dumps(zipmeta,ensure_ascii=False,indent=2));z.write(outdir/'verification.json','wangshu-v2/verification.json')
with zipfile.ZipFile(zipname,'a',zipfile.ZIP_DEFLATED) as z:
 if (outdir/'preview-page-check.json').exists():z.write(outdir/'preview-page-check.json','wangshu-v2/preview-page-check.json')
with zipfile.ZipFile(zipname) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.rsplit('/',1)[-1].startswith('ws_') and n.endswith('.png')])==10
 for url in re.findall(r'(?:src|href)="([^"]+)"',z.read('wangshu-v2/preview.html').decode()):assert 'wangshu-v2/'+url in z.namelist(),url
print('Checked10 transparent512 stickers,2 matching repo locations,overview/gallery and ZIP:',zipname,zipname.stat().st_size)
