from PIL import Image
import os
import glob
from tqdm import tqdm
import six


in_dir = "./adkImages/"
out_dir = "./assetsADK/"
inp = glob.glob(os.path.join(in_dir, "*.jpg")) 
for i, inp in enumerate(tqdm(inp)):
	if isinstance(inp, six.string_types):
		out_fname = os.path.basename(inp)
		im = Image.open(inp)
		resized = im.resize((473,473), resample=Image.NEAREST)
		resized.save(out_dir + out_fname, "JPEG")


