for fname in fnames:
	if fname.startswith(badprefix):
		os.rename(fname,fname.replace(badprefix,'',1))