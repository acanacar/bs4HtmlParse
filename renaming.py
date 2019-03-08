import glob, os


def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        print(pathAndFilename)
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        title = title[:-14]+title[-7:]
        print('ext: ',ext)
        os.rename(pathAndFilename,
                  os.path.join(dir, titlePattern % title))


rename(r'/home/cem/PycharmProjects/htmlParseInf/Bilanco-zip/excels', r'*.html', r'%s.html')
