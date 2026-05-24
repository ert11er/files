from urllib.parse import urlparse
import json, requests, sys, re

# Cleaned list: Removed duplicates (like apptesters) and fixed malformed strings
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
    "https://bit.ly/Quantumsource",
    "https://bit.ly/wuxuslibraryplus",
    "https://altstore.9ani.app",
    "https://bit.ly/40Isul6",
    "https://repo.starfiles.co/public?gbox",
    "https://repo.apptesters.org"
]

sources_requiring_ua = {
    "https://ipa.cypwn.xyz/sidestore.json"
}

user_agent = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Safari/537.36"

altsource = {
    "name": "Ert Source",
    "iconURL": "https://i.imgur.com/pqIZoZo.jpeg",
    "identifier": "com.ert.source",
    "sourceURL": "https://files-private.vercel.app/altsource.json",
    "apps": [],
    "news": []
}

def is_valid_url(url):
    if not url or not isinstance(url, str):
        return False
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False

def sanitize_app(app):
    if not isinstance(app, dict):
        return None

    def clean_text(text):
        if not text or not isinstance(text, str):
            return text
        return re.sub(r'[^\w\s]', '', text).strip()

    if "name" in app:
        app["name"] = clean_text(app["name"])
    if "subtitle" in app:
        app["subtitle"] = clean_text(app["subtitle"])
    if "caption" in app:
        app["caption"] = clean_text(app["caption"])

    if not app.get("name") or not app.get("bundleIdentifier"):
        return None

    if "iconURL" in app and not is_valid_url(app["iconURL"]):
        app["iconURL"] = "https://placehold.co/512x512"
    
    if "screenshotURLs" in app and isinstance(app["screenshotURLs"], list):
        app["screenshotURLs"] = [url for url in app["screenshotURLs"] if is_valid_url(url)]
    
    # Strictly ensure versions structure exists and handles size constraints
    if "versions" in app and isinstance(app["versions"], list) and len(app["versions"]) > 0:
        for version in app["versions"]:
            if version.get("size", 0) == 0:
                version["size"] = 40756573
    else:
        # AltStore crashes if an app has 0 version definitions
        return None

    content_string = (app.get("name", "") + app.get("subtitle", "") + app.get("localizedDescription", "")).lower()
    if "patreon" in content_string:
        return None

    return app
    
all_collected_apps = []

# Deduplicate sources array dynamically to prevent recursive scraping loops
other_sources = list(dict.fromkeys(other_sources))

for source_url in other_sources:
    try:
        print(f"Fetching data from {source_url}")
        headers = {"User-Agent": user_agent} if source_url in sources_requiring_ua else {}
        response = requests.get(source_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Safely capture JSON errors
        try:
            source_data = response.json()
        except ValueError:
            print(f"  Skipping non-JSON response from: {source_url}")
            continue
        
        if not isinstance(source_data, dict):
            continue

        is_pal = source_data.get("isPAL") is True or any(app.get("marketplaceID") for app in source_data.get("apps", [])) if isinstance(source_data.get("apps"), list) else False
        if is_pal or "palsource" in source_url.lower():
            print(f"  Skipping AltStore PAL source: {source_url}")
            continue
            
        if "apps" in source_data and isinstance(source_data["apps"], list):
            count = 0
            for app in source_data["apps"]:
                if app.get("paywall") or app.get("closedSource") or app.get("palOnly"):
                    continue
                    
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

apps_by_bid = {}
for app in all_collected_apps:
    bid = app.get("bundleIdentifier")
    if bid not in apps_by_bid:
        apps_by_bid[bid] = []
    apps_by_bid[bid].append(app)

final_apps = []
used_bundle_identifiers = set()

for bid, group in apps_by_bid.items():
    group.sort(key=lambda x: get_version_tuple(x.get("version")), reverse=True)
    if not group: continue
    
    newest_app = group[0]
    newest_version_tuple = get_version_tuple(newest_app.get("version"))
    candidates = [a for a in group if get_version_tuple(a.get("version")) == newest_version_tuple]
    
    for i, app in enumerate(candidates):
        # Truncate history to avoid bloating AltStore client memory
        if "versions" in app and isinstance(app["versions"], list):
            app["versions"] = app["versions"][:1]
            
        if i > 0:
            app["name"] = f"{app.get('name')} {i}"
            app["bundleIdentifier"] = f"{app.get('bundleIdentifier')}{i}"
            
        # Guarantee uniqueness across the whole ecosystem output file
        current_bid = app["bundleIdentifier"]
        if current_bid not in used_bundle_identifiers:
            used_bundle_identifiers.add(current_bid)
            final_apps.append(app)

altsource["apps"] = final_apps
altsource["apps"].sort(key=lambda x: x.get('name', '').lower())

# Save minified file clean-packed without broken key structures
with open("altsource.json", "w", encoding="utf-8") as f:
    json.dump(altsource, f, separators=(',', ':'), ensure_ascii=False)

print(f"\nSuccessfully generated parsing-safe altsource.json with {len(final_apps)} apps.")
