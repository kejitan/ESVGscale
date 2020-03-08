from PIL import Image 
import glob, os
from tqdm import tqdm
import six

in_dir = "./assetsADK/"
out_dir = "./pngADK/"

inp = glob.glob(os.path.join(in_dir, "*.jpg")) 
for i, inp in enumerate(tqdm(inp)):
	if isinstance(inp, six.string_types):
		out_fname = os.path.basename(inp)
		file, ext = os.path.splitext(out_fname)
		im = Image.open(inp)
		im.save(out_dir + file + ".png", "PNG")

