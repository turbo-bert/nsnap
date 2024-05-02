import requests
import json
import time


def replace_special_chars(src):
    mapping = {}
    mapping['&quot;'] = "-";
    mapping['ä'] = "ae";
    mapping['ü'] = "ue";
    mapping['ö'] = "oe";
    mapping['Ä'] = "Ae";
    mapping['Ü'] = "Ue";
    mapping['Ö'] = "Oe";
    mapping['ß'] = "ss";
    mapping['&'] = " und ";
    n=src
    for k in mapping.keys():
        n = n.replace(k, mapping[k])
    return n


def drop_special_chars(src):
    n=""
    alp = "0123456789,.-:/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    for c in src:
        if c in alp:
            n+=c
    while n.find("  ") >= 0:
        n = n.replace("  ", " ")
    return n.strip()


def extract_firsttag_inner(src, tag_name):
    o_tag = "<%s>" % tag_name
    c_tag = "</%s>" % tag_name
    pos1 = src.find(o_tag)
    pos2 = src.find(c_tag)
    body = src[pos1+len(o_tag):pos2]
    return body


def rss_generic(src, object_id, link_divider=None, strip_title_prefix=None, related_to=None):
    # with open("%s.txt" % object_id, "w") as f:
    #     f.write(src)
    title_cols = src.split("<item>")[1:]
    articles = []
    for t in title_cols:
        z_title = extract_firsttag_inner(t, "title")
        z_title = replace_special_chars(z_title)
        z_title = drop_special_chars(z_title)
        z_title = z_title.strip()
        if strip_title_prefix is not None and z_title.startswith(strip_title_prefix):
            z_title = z_title[len(strip_title_prefix):].strip()
        z_link = extract_firsttag_inner(t, "link")
        z_link = z_link.strip()
        z = {"title": z_title, "link": z_link, "epoch_timestamp": int(time.time()), "related_to": related_to}
        if link_divider is not None:
            z["link"] = z_link.split(link_divider)[0]
        articles.append(z)
    with open("%s.js" % object_id, "w") as f:
        f.write(json.dumps(articles, indent=4))

rss_generic(src=requests.get("https://www.spiegel.de/schlagzeilen/tops/index.rss").text, object_id="spiegel", link_divider="#", strip_title_prefix=None, related_to="country:de")
rss_generic(src=requests.get("https://www.heise.de/security/rss/news.rdf").text, object_id="heise-security", link_divider='?', strip_title_prefix=None, related_to="topic:it-security")
rss_generic(src=requests.get("https://www.aachener-zeitung.de/lokales/region-aachen/aachen/rss/").text, object_id="aachener-nachrichten-aachen", link_divider=None, strip_title_prefix="CDATA", related_to="geo:50.774536031739515:6.083623744229666")
rss_generic(src=requests.get("https://www.aachener-zeitung.de/lokales/region-aachen/herzogenrath/rss/").text, object_id="aachener-nachrichten-herzogenrath", link_divider=None, strip_title_prefix="CDATA", related_to="geo:50.86049020348183:6.083922990502097")
rss_generic(src=requests.get("https://rp-online.de/nrw/staedte/grevenbroich/feed.rss").text, object_id="rp-grevenbroich", link_divider=None, strip_title_prefix=None, related_to="geo:51.18267853983402:6.581391111751763")
rss_generic(src=requests.get("https://rp-online.de/feed.rss").text, object_id="rp", link_divider=None, strip_title_prefix=None, related_to="country:de")
rss_generic(src=requests.get("https://rss.sueddeutsche.de/alles").text, object_id="sueddeutsche", link_divider=None, strip_title_prefix="CDATA", related_to="country:de")
rss_generic(src=requests.get("https://www.stern.de/feed/standard/all/").text, object_id="stern", link_divider='?', strip_title_prefix=None, related_to="country:de")
rss_generic(src=requests.get("http://www.bild.de/rss-feeds/rss-16725492,feed=news.bild.html").text, object_id="bild-news", link_divider=None, strip_title_prefix="CDATA", related_to="country:de")
rss_generic(src=requests.get("https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml").text, object_id="tagesschau", link_divider=None, strip_title_prefix=None, related_to="country:de")
