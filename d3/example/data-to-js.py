import pandas as pd
import sys

NO_OF_WORDS = 500

f = open("files/NewsDataUnigramDaily")
amazing = f.readlines()
df = pd.DataFrame([[" ".join(i.split()[:1]),int(i.split()[-1])] for i in amazing]).sort_values(1,ascending=False)[1:]
a  = ["\t".join(list([str(z) for z in j])) for i,j in df.reset_index(drop=True).iterrows()]
writer = ["var unigram_daily_news = [\n"]+["{text:'"+" ".join(i.split()[:1])+"', size: "+i.split()[-1]+"},\n" for i in a][:NO_OF_WORDS] + ["];"]
with open("unigram_daily_news.js","w") as f:
    f.writelines(writer)

top10 = list(df.reset_index(drop=True)[:10][0])

f = open("files/NewsDataBigramDaily")
amazing = f.readlines()
amazing2 = [i for i in amazing if (i.split()[0] in top10) or (i.split()[1] in top10)]
df = pd.DataFrame([[" ".join(i.split()[:2]),int(i.split()[-1])] for i in amazing2]).sort_values(1,ascending=False)
a  =["\t".join(list([str(z) for z in j])) for i,j in df.reset_index(drop=True).iterrows()]
writer = ["var bigram_daily_news = [\n"]+["{text:'"+" ".join(i.split()[:2])+"', size: "+i.split()[-1]+"},\n" for i in a][:NO_OF_WORDS] + ["];"]
with open("bigram_daily_news.js","w") as f:
    f.writelines(writer)


f = open("files/TwitterDataUnigramDaily")
amazing = f.readlines()
df = pd.DataFrame([[" ".join(i.split()[:1]),int(i.split()[-1])] for i in amazing]).sort_values(1,ascending=False)[1:]
a  = ["\t".join(list([str(z) for z in j])) for i,j in df.reset_index(drop=True).iterrows()]
writer = ["var unigram_daily_twitter = [\n"]+["{text:'"+" ".join(i.split()[:1])+"', size: "+i.split()[-1]+"},\n" for i in a][:NO_OF_WORDS] + ["];"]
with open("unigram_daily_twitter.js","w") as f:
    f.writelines(writer)

top10 = list(df.reset_index(drop=True)[:10][0])

f = open("files/TwitterDataBigramDaily")
amazing = f.readlines()
amazing2 = [i for i in amazing if (i.split()[0] in top10) or (i.split()[1] in top10)]
df = pd.DataFrame([[" ".join(i.split()[:2]),int(i.split()[-1])] for i in amazing2]).sort_values(1,ascending=False)
a  =["\t".join(list([str(z) for z in j])) for i,j in df.reset_index(drop=True).iterrows()]
writer = ["var bigram_daily_twitter = [\n"]+["{text:'"+" ".join(i.split()[:2])+"', size: "+i.split()[-1]+"},\n" for i in a][:NO_OF_WORDS] + ["];"]
with open("bigram_daily_twitter.js","w") as f:
    f.writelines(writer)

f = open("files/NewsDataUnigramWeekly")
amazing = f.readlines()
df = pd.DataFrame([[" ".join(i.split()[:1]),int(i.split()[-1])] for i in amazing]).sort_values(1,ascending=False)[1:]
a  = ["\t".join(list([str(z) for z in j])) for i,j in df.reset_index(drop=True).iterrows()]
writer = ["var unigram_weekly_news = [\n"]+["{text:'"+" ".join(i.split()[:1])+"', size: "+i.split()[-1]+"},\n" for i in a][:NO_OF_WORDS] + ["];"]
with open("unigram_weekly_news.js","w") as f:
    f.writelines(writer)

top10 = list(df.reset_index(drop=True)[:10][0])

f = open("files/NewsDataBigramWeekly")
amazing = f.readlines()
amazing2 = [i for i in amazing if (i.split()[0] in top10) or (i.split()[1] in top10)]
df = pd.DataFrame([[" ".join(i.split()[:2]),int(i.split()[-1])] for i in amazing2]).sort_values(1,ascending=False)
a  =["\t".join(list([str(z) for z in j])) for i,j in df.reset_index(drop=True).iterrows()]
writer = ["var bigram_weekly_news = [\n"]+["{text:'"+" ".join(i.split()[:2])+"', size: "+i.split()[-1]+"},\n" for i in a][:NO_OF_WORDS] + ["];"]
with open("bigram_weekly_news.js","w") as f:
    f.writelines(writer)


f = open("files/TwitterDataUnigramWeekly")
amazing = f.readlines()
df = pd.DataFrame([[" ".join(i.split()[:1]),int(i.split()[-1])] for i in amazing]).sort_values(1,ascending=False)[1:]
a  = ["\t".join(list([str(z) for z in j])) for i,j in df.reset_index(drop=True).iterrows()]
writer = ["var unigram_weekly_twitter = [\n"]+["{text:'"+" ".join(i.split()[:1])+"', size: "+i.split()[-1]+"},\n" for i in a][:NO_OF_WORDS] + ["];"]
with open("unigram_weekly_twitter.js","w") as f:
    f.writelines(writer)

top10 = list(df.reset_index(drop=True)[:10][0])

f = open("files/TwitterDataBigramWeekly")
amazing = f.readlines()
amazing2 = [i for i in amazing if (i.split()[0] in top10) or (i.split()[1] in top10)]
df = pd.DataFrame([[" ".join(i.split()[:2]),int(i.split()[-1])] for i in amazing2]).sort_values(1,ascending=False)
a  =["\t".join(list([str(z) for z in j])) for i,j in df.reset_index(drop=True).iterrows()]
writer = ["var bigram_weekly_twitter = [\n"]+["{text:'"+" ".join(i.split()[:2])+"', size: "+i.split()[-1]+"},\n" for i in a][:NO_OF_WORDS] + ["];"]
with open("bigram_weekly_twitter.js","w") as f:
    f.writelines(writer)
