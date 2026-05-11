from urllib.parse import urlparse
import json, requests, sys, re

other_sources = [
    "https://therealfoxster.github.io/altsource/apps.json",
    "https://fastsign.dev/repo.json",
    "https://fastsign.dev/repo.lite.json",
    "https://fastsign.dev/repo.lite.altstore.json",
    "https://flyinghead.github.io/flycast-builds/altstore.json",
    "https://raw.githubusercontent.com/Neoncat-OG/TrollStore-IPAs/main/apps_esign.json",
    "https://qnblackcat.github.io/AltStore/apps.json",
    "https://pokemmo.eu/altstore/",
    "https://altstore.oatmealdome.me",
    "https://wuxu1.github.io/wuxu-complete-plus.json",
    "https://ipa.cypwn.xyz/cypwn.json",
    "https://community-apps.sidestore.io/sidecommunity.json",
    "https://tiny.one/SpotC",
    "https://raw.githubusercontent.com/arichornloveralt/arichornloveralt.github.io/main/apps.json",
    "https://raw.githubusercontent.com/whoeevee/EeveeSpotify/swift/repo.json",
    "https://aio.yippee.rip/repo.json",
    "https://css.eyz.ink/appstore",
    "https://xitrix.github.io/iTorrent/AltStore.json",
    "https://ish.app/altstore.json",
    "https://repository.apptesters.org",
    "https://repo.whoeevee.com/esign",
    "https://repo.madari.media/nightly/repo.json",
    "https://github.com/dvntm0/AltStore/raw/refs/heads/main/feather.json",
    "https://raw.githubusercontent.com/notrifty1/riftysrepo/refs/heads/main/reposource.json",
    "https://altstore.oatmealdome.me/",
    "https://raw.githubusercontent.com/driftywinds/driftywinds.github.io/master/AltStore/apps.json",
    "https://web.archive.org/web/20240828224000/https://raw.githubusercontent.com/swaggyP36000/TrollStore-IPAs/main/apps_esign.json",
    "https://repo.realmzer.xyz",
    "https://raw.githubusercontent.com/Gliddd4/gliddd4-repo/refs/heads/main/app.json",
    "https://repo.chungchi365.com/repo.json",
    "https://raw.githubusercontent.com/zigwangles/zigwangles-repo/refs/heads/main/app-repo.json",
    "https://raw.githubusercontent.com/AntonP29/AntonP29-Repo/refs/heads/main/repo.json",
    "https://repo.owo.network/",
    "https://balackburn.github.io/Apollo/apps.json",
    "https://apps.altstore.io/",
    "https://bit.ly/Altstore-complete",
    "https://appmarket.tech/altstore.json",
    "https://raw.githubusercontent.com/Auties00/Artemis/refs/heads/main/source.json",
    "https://bunduuk.github.io/altstore-source/apps.json",
    "https://get.furaffinity.app/altstore-world/",
    "https://ipa.cypwn.xyz/cypwn_ts.json",
    "https://enmity-mod.github.io/repo/altstore.json",
    "https://github.com/khcrysalis/Feather/raw/main/app-repo.json",
    "https://therealfoxster.github.io/altsource/apps.json",
    "https://hottubapp.io/altstore",
    "https://altstore.ignitedemulator.com",
    "https://raw.githubusercontent.com/Nyasami/Ksign/refs/heads/main/repo.json",
    "https://alts.lao.sb",
    "https://buildbot.libretro.com/stable/altstore.json",
    "https://raw.githubusercontent.com/LiveContainer/LiveContainer/refs/heads/main/apps.json",
    "https://theodyssey.dev/altstore/odysseysource.json",
    "https://raw.githubusercontent.com/vizunchik/AltStoreRus/master/apps.json",
    "https://alt.crystall1ne.dev",
    "https://pokemmo.com/altstore/",
    "https://provenance-emu.com/apps.json",
    "https://quarksources.github.io/dist/quantumsource.min.json",
    "https://bit.ly/Quantumsource-plus",
    "https://quarksources.github.io/quarksource-cracked.json",
    "https://randomblock1.com/altstore/apps.json",
    "https://spotc-repo.yodaluca.dev/AltStore%20Repo.json",
    "https://taurine.app/altstore/taurinestore.json",
    "https://alt.getutm.app",
    "https://wuxu1.github.io/wuxu-complete.json",
    "https://raw.githubusercontent.com/Balackburn/YTLitePlusAltstore/main/apps.json",
    "https://azu0609.github.io/repo/altstore_repo.json",
    "https://raw.githubusercontent.com/cbruegg/altstore-source/refs/heads/main/source.json",
    "https://raw.githubusercontent.com/driftywinds/driftywinds.github.io/master/AltStore/nyx.json",
    "https://raw.githubusercontent.com/driftywinds/driftywinds.github.io/master/AltStore/theta.json",
    "https://repo.ethsign.fyi",
    "https://raw.githubusercontent.com/lo-cafe/winston-altstore/main/apps.json",
    "https://esign.yyyue.xyz/app.json",
    "https://alt.thatstel.la/",
    "https://apps.nabzclan.vip/repos/altstore.php",
    "https://apps.sidestore.io/",
    "https://binnichtaktiv.signapp.me/repo/esign.json",
    "https://burritosoftware.github.io/altstore/channels/burritosource.json",
    "https://connect.sidestore.io/apps.json",
    "https://cranci.tech/repo.json",
    "https://driftywinds.github.io/repos/esign.json",
    "https://dvntm0.github.io/AltStore/raw/refs/heads/main/esign.json",
    "https://floridaman7588.me/altjb/altsource.json",
    "https://gbox.run/Public/Source.json",
    "https://hann8n.github.io/JackCracks/MovieboxPro.json",
    "https://ia601404.us.archive.org/11/items/ms_20220903/MS.json",
    "https://ia601407.us.archive.org/11/items/ms_20220903/MS.json",
    "https://ia601505.us.archive.org/10/items/motoca-store/Motoca%20Store.json",
    "https://ikghd.site/repo.json",
    "https://ipa.thuthuatjb.com/repo",
    "https://ittza7aa.com/repo.json",
    "https://lo-cafe/winston-altstore/main/apps.json",
    "https://madari.media/nightly/repo.json",
    "https://nabzclan.vip/repos/esign.php",
    "https://qingsongqian.github.io/all.html",
    "https://quarksources.github.io/quantumsource++.json",
    "https://quarksources.github.io/quantumsource.json",
    "https://raw.githubusercontent.com/Omni-Development/The-Omni-Repository/refs/heads/main/app-repo.json",
    "https://raw.githubusercontent.com/RealBlackAstronaut/CelestialRepo/main/CelestialRepo.json",
    "https://raw.githubusercontent.com/TheNightmanCodeth/chromium-ios/master/altstore-source.json",
    "https://raw.githubusercontent.com/WhySooooFurious/Ultimate-Sideloading-Guide/refs/heads/main/app-repo.json",
    "https://raw.githubusercontent.com/YourName028/System-Apps/main/repo.json",
    "https://raw.githubusercontent.com/actuallyaridan/NeoFreeBird/refs/heads/main/AltSource.json",
    "https://raw.githubusercontent.com/arichornloverALT/arichornloveralt.github.io/main/apps2.json",
    "https://raw.githubusercontent.com/jay-goobuh/samhub/main/apps",
    "https://raw.githubusercontent.com/qnblackcat/AltStore/gh-pages/apps.json",
    "https://raw.githubusercontent.com/sinceohsix/lcdl-repo/refs/heads/main/repo.json",
    "https://raw.githubusercontent.com/ssalggnikool/.github/refs/heads/main/b.json",
    "https://repo.starfiles.co",
    "https://repo.ucerts.io",
    "https://repo.zsign.app/repo.json",
    "https://repos.yattee.stream/alt/apps.json",
    "https://rickowens.su/repo.json",
    "https://tweakrain.pages.dev/ios/altstore.json",
    "https://web.archive.org/web/20210225095501if_/https://appybois.com/",
    "https://web.archive.org/web/20250310010244if_/https://repo.realmzer.xyz/",
    "https://website.burrito.software/altstore/channels/burritosource.json",
    "https://www.sachcharak.com/esign/repo/RAK.json",
    "https://github.com/LiveContainer/LiveContainer/releases/download/nightly/apps_nightly.json",
    "https://connect.sidestore.io/",
    "https://raw.githubusercontent.com/LiveContainer/LiveContainer/refs/heads/main/apps.json",
    "https://bit.ly/Quantumsource",
    "https://bit.ly/Quantumsource-plus",
    "https://bit.ly/wuxuslibraryplus",
    "https://bit.ly/Altstore-complete",
    "https://altstore.oatmealdome.me/",
    "https://flyinghead.github.io/flycast-builds/altstore.json",
    "https://burritosoftware.github.io/altstore/channels/burritosource.json",
    "https://alts.lao.sb",
    "https://floridaman7588.me/altjb/altsource.json",
    "https://pokemmo.com/altstore/",
    "https://alt.getutm.app",
    "https://theodyssey.dev/altstore/odysseysource.json",
    "https://taurine.app/altstore/taurinestore.json",
    "https://altstore.9ani.app",
    "https://randomblock1.com/altstore/apps.json",
    "https://provenance-emu.com/apps.json",
    "https://bit.ly/40Isul6",
    "https://ish.app/altstore.json",
    "https://community-apps.sidestore.io/sidecommunity.json",
    "https://repo.starfiles.co/public?gbox",
    "https://repo.apptesters.org"
]

# Sources that require a user agent
sources_requiring_ua = {
"https://ipa.cypwn.xyz/sidestore.json"
}

user_agent = "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +https://www.google.com/bot.html)"


altsource = {
    "name": "Ert Source",
    "identifier": "com.ert.source",
    "sourceURL": "https://files-private.vercel.app/altsource.json",
    "apps": [],
    "news": []
}

def is_valid_url(url):
    """Check if URL is a valid absolute URL"""
    if not url or not isinstance(url, str):
        return False
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False

def sanitize_app(app):
    """Sanitize app data, removing invalid URLs and filtering symbols from text"""
    if not isinstance(app, dict):
        return None

    # Sembolleri ( !, ?, # vb.) temizlemek için yardımcı fonksiyon
    def clean_text(text):
        if not text or not isinstance(text, str):
            return text
        # Sadece alfanümerik karakterleri ve boşlukları tutar
        return re.sub(r'[^\w\s]', '', text).strip()

    # Başlık (name), Altyazı (subtitle) ve varsa Caption kısımlarını filtrele
    if "name" in app:
        app["name"] = clean_text(app["name"])
    
    if "subtitle" in app:
        app["subtitle"] = clean_text(app["subtitle"])
        
    if "caption" in app:
        app["caption"] = clean_text(app["caption"])

    # İsim boşsa veya semboller silinince boş kaldıysa iptal et
    if not app.get("name"):
        return None

    # URL Kontrolleri
    if "iconURL" in app:
        if not is_valid_url(app["iconURL"]):
            app["iconURL"] = "https://placehold.co/512x512"
    
    if "screenshotURLs" in app and isinstance(app["screenshotURLs"], list):
        app["screenshotURLs"] = [url for url in app["screenshotURLs"] if is_valid_url(url)]
    
    # Zorunlu alan kontrolü
    if not app.get("bundleIdentifier"):
        return None
    
    return app
    
all_collected_apps = []

for source_url in other_sources:
    try:
        print(f"Fetching data from {source_url}")
        headers = {}
        if source_url in sources_requiring_ua:
            headers["User-Agent"] = user_agent
        response = requests.get(source_url, headers=headers, timeout=10)
        response.raise_for_status()
        source_data = response.json()
        
        if "apps" in source_data:
            count = 0
            for app in source_data["apps"]:
                sanitized = sanitize_app(app)
                if sanitized:
                    all_collected_apps.append(sanitized)
                    count += 1
            print(f"  Collected {count} apps from {source_data.get('name', source_url)}")
    except Exception as e:
        print(f"  Error fetching data from {source_url}: {e}")

def get_version_tuple(v):
    if not v: return (0,)
    parts = re.findall(r'\d+', str(v))
    return tuple(int(x) for x in parts) if parts else (0,)

blacklist_words = []

if blacklist_words:
    filtered_apps = []
    for app in all_collected_apps:
        description = (app.get("localizedDescription") or "").lower()
        if not any(word.lower() in description for word in blacklist_words):
            filtered_apps.append(app)
        else:
            print(f"  Filtering out {app.get('name')} due to blacklisted word in description.")
    all_collected_apps = filtered_apps

apps_by_bid = {}
for app in all_collected_apps:
    bid = app.get("bundleIdentifier")
    if bid not in apps_by_bid:
        apps_by_bid[bid] = []
    apps_by_bid[bid].append(app)

final_apps = []
for bid, group in apps_by_bid.items():
    group.sort(key=lambda x: get_version_tuple(x.get("version")), reverse=True)
    if not group: continue
    
    newest_app = group[0]
    newest_version_tuple = get_version_tuple(newest_app.get("version"))
    candidates = [a for a in group if get_version_tuple(a.get("version")) == newest_version_tuple]
    
    for i, app in enumerate(candidates):
        if i > 0:
            app["name"] = f"{app.get('name')} {i}"
            app["bundleIdentifier"] = f"{app.get('bundleIdentifier')}{i}"
        final_apps.append(app)

altsource["apps"] = final_apps
altsource["apps"].sort(key=lambda x: x.get('name', '').lower())

with open("altsource.json", "w", encoding="utf-8") as f:
    json.dump(altsource, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully generated altsource.json with {len(final_apps)} apps.")
