import packaging.version

class Config:
    GAME_VERSION_NAME = packaging.version.Version("2.23.0")
    
    _REMOVED_SONGS = {
        # "monitoring": "2.23.0",
        # "rokutyounen": "2.23.0",
        # "wildcard": "2.23.0"
    }
    REMOVED_SONGS = {song_id: packaging.version.Version(version) for song_id, version in _REMOVED_SONGS.items()}
    
    _CHANGE_SONGS = {
        "rokutyounen": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 14.1,
                "IV": 13.3,
                "III": 10.2
            }
        },
        "akari-koushu": {
            "version": "2.23.0",
            "rating": {
                "IV": 14.3,
                "III": 12.2
            }
        },
        "emulisy": {
            "version": "2.23.0",
            "rating": {
                "IV": 14.1,
                "III": 11.7
            }
        },
        "galactic-warzone": {
            "version": "2.23.0",
            "rating": {
                "IV": 14.3,
                "III": 11.7
            }
        },
        "way-home": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 14.1,
                "III": 11.5
            }
        },
        "distant-call": {
            "version": "2.23.0",
            "rating": {
                "IV": 14
            }
        },
        "imagined-flight": {
            "version": "2.23.0",
            "rating": {
                "IV": 14.0,
                "III": 11.3
            }
        },
        "lunatixxx-gear": {
            "version": "2.23.0",
            "rating": {
                "IV": 14.2,
                "III": 11.5
            }
        },
        "abstruse-dilemma": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.9,
                "III": 12,
                "II": 6,
                "I": 2
            }
        },
        "binary": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 13.9,
                "IV": 12.9
            }
        },
        "corps-sans-organes": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.9,
                "III": 12
            }
        },
        "stage-5": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 13.9,
                "IV": 12.9
            }
        },
        "aleph-0": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 13.5,
                "IV": 12.4,
                "III": 11.4
            }
        },
        "brave-road": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.8,
                "III": 12.4
            }
        },
        "muten-shorai": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 13.8,
                "IV": 12.8
            }
        },
        "recollection": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.8,
                "III": 11.6
            }
        },
        "take": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.7,
                "III": 10.3
            }
        },
        "uchronia": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 13.7,
                "III": 11.5
            }
        },
        "dual-doom-deathmatch": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.9,
                "III": 11.8
            }
        },
        "echoes-of-the-forest": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5
            }
        },
        "hydra": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.7,
                "III": 10.5
            }
        },
        "kakuriyo": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.6,
                "III": 10
            }
        },
        "rush-e": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.7
            }
        },
        "yusui": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.7
            }
        },
        "chunlian": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.6
            }
        },
        "distorted-fate": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.6,
                "III": 11.5
            }
        },
        "heartache": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.9,
                "III": 10
            }
        },
        "inverted-world": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.6,
                "III": 11.4
            }
        },
        "invisible-frenzy": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.8,
                "III": 11.4
            }
        },
        "welcome-ssspooky": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.8,
                "III": 11.8
            }
        },
        "cyanine": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5
            }
        },
        "destr0yer": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5
            }
        },
        "enter-magical-code": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5
            }
        },
        "eventide-rush": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5
            }
        },
        "innocence-keeper": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5,
                "III": 11.6
            }
        },
        "our-message": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5
            }
        },
        "rrharil": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5,
                "III": 11.8
            }
        },
        "sekigae-yatta": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5
            }
        },
        "aventyr": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 13.4,
                "IV": 11.4
            }
        },
        "black-lair": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4
            }
        },
        "cynthia": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.2
            }
        },
        "daydream": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.2,
                "III": 10.9
            }
        },
        "hyouryu": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4
            }
        },
        "meiseki-yume-nite": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4
            }
        },
        "muen": {
            "version": "2.23.0",
            "rating": {
                "IV": 13
            }
        },
        "saku-hoshiboshi": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 13.3,
                "IV": 12.1
            }
        },
        "tenq": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.3
            }
        },
        "vector": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4
            }
        },
        "whence": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4
            }
        },
        "yinmn-blue": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4
            }
        },
        "cosmic-railroad": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.3
            }
        },
        "cosmogyral": {
            "version": "2.23.0",
            "rating": {
                "IV": 13
            }
        },
        "dextroy": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.2,
                "III": 12.3
            }
        },
        "energy-synergy-matrix": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.3
            }
        },
        "flutter-echo": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.3
            }
        },
        "hold-your-fire": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1
            }
        },
        "quaoar": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5,
                "III": 11.3
            }
        },
        "shiragiku": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.2
            }
        },
        "ultra-synergy-matrix": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.5,
                "III": 11.3
            }
        },
        "alfheims-faith": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 13.2,
                "IV": 12.5,
                "III": 10.5
            }
        },
        "alive": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.2
            }
        },
        "bounce-the-tech": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.2
            }
        },
        "brain-power": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1
            }
        },
        "far-side-of-the-moon": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.2
            }
        },
        "give-me-your-love": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.2
            }
        },
        "junky-night-town-orchestra": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.2
            }
        },
        "manifold-hypothesis": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4
            }
        },
        "nyarlathotep": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.9
            }
        },
        "sense": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1
            }
        },
        "tianlingling": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1
            }
        },
        "9876734123": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.3
            }
        },
        "aria": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.3
            }
        },
        "feast-from-the-east": {
            "version": "2.23.0",
            "rating": {
                "IV": 13
            }
        },
        "go-escape": {
            "version": "2.23.0",
            "rating": {
                "IV": 13
            }
        },
        "in-a-diabolic-manner": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4,
                "III": 11.4
            }
        },
        "inner-norm": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1
            }
        },
        "koki-chant": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.3
            }
        },
        "kouen": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1
            }
        },
        "marble-joker": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4
            }
        },
        "on-and-on": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.3
            }
        },
        "simulated": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4
            }
        },
        "alice-in-a-xxxxxxxx": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.4,
                "III": 11
            }
        },
        "androgynos2": {
            "version": "2.23.0",
            "rating": {
                "IV": 13
            }
        },
        "android-girl": {
            "version": "2.23.0",
            "rating": {
                "IV": 13
            }
        },
        "bassline-yatteru-lol": {
            "version": "2.23.0",
            "rating": {
                "IV": 13
            }
        },
        "calorific-refract": {
            "version": "2.23.0",
            "rating": {
                "IV": 13,
                "III": 10.3
            }
        },
        "ego-eimi": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.9,
                "III": 10
            }
        },
        "party-before-hibernation": {
            "version": "2.23.0",
            "rating": {
                "IV": 13,
                "III": 11.4
            }
        },
        "rip": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.3
            }
        },
        "a-philosophical-wanderer": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1,
                "III": 10.7
            }
        },
        "brain-crusher": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1
            }
        },
        "chronomia": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "cosmic-voyage": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1
            }
        },
        "heavens-cage": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1,
                "III": 10.4
            }
        },
        "hushwave-symptoms": {
            "version": "2.23.0",
            "rating": {
                "IV_Alpha": 13.1
            }
        },
        "kami-ppoi-na": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.9
            }
        },
        "magenta-potion": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.1
            }
        },
        "steadfast": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "turning-point": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.9
            }
        },
        "vertexion": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.9
            }
        },
        "antagonism": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.5
            }
        },
        "beat-rise": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "fantasia-sonata-god-dance": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "infection": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "link-x-lins": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "mirukiuei-o-tadotte": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "mistilteinn": {
            "version": "2.23.0",
            "rating": {
                "IV": 13
            }
        },
        "otome-dissection": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "skyward-echo": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "suito": {
            "version": "2.23.0",
            "rating": {
                "III": 12.4,
                "II": 9.3
            }
        },
        "toys-nightlife-area": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "water-recreation": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "windsurfer": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "xlix": {
            "version": "2.23.0",
            "rating": {
                "III": 12.4
            }
        },
        "arbitration": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "blue-ixia": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.6
            }
        },
        "broomstick-adventure": {
            "version": "2.23.0",
            "rating": {
                "IV": 13
            }
        },
        "deus-judicium": {
            "version": "2.23.0",
            "rating": {
                "III": 12.4
            }
        },
        "eos": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.6
            }
        },
        "from-zero": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.6,
                "III": 10.6
            }
        },
        "gecko": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "iza-mairimasu": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "life-flashes-before-weeb-eyes": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "milk": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.4
            }
        },
        "my-heaven-magical-mix": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "re-end-of-a-dream": {
            "version": "2.23.0",
            "rating": {
                "III": 12.3
            }
        },
        "secret-illumination-aura-remix": {
            "version": "2.23.0",
            "rating": {
                "IV": 13.9,
                "III": 10.5
            }
        },
        "sweet-and-astringent-dreams": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "because-of-you": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.5
            }
        },
        "blackhole": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.2
            }
        },
        "blastrick": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "devil-la6ue": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.5
            }
        },
        "ef4123": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.6
            }
        },
        "flashdance": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.5
            }
        },
        "luminosity": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "maho-shojo-intai-sengen": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.5
            }
        },
        "memory-of-sunrise": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "my-story": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.6
            }
        },
        "nighttheater": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.6
            }
        },
        "nini": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.6
            }
        },
        "one-way-street": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.6
            }
        },
        "snowbound-flight": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "time-keeper": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.8
            }
        },
        "wakatterukedo": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.6
            }
        },
        "centimental": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "csqn": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.4
            }
        },
        "hoshizora-toraberu": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.5
            }
        },
        "smile-miles": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "sonic-surge": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.5
            }
        },
        "true": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "vesta": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "with-u": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "chant-shite": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.1
            }
        },
        "cross-soul": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.4
            }
        },
        "internet-overdose": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.2
            }
        },
        "rainy-day": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.4
            }
        },
        "re-prosperitas": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.3,
                "III": 10
            }
        },
        "rocket-lanterns": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.3
            }
        },
        "ruby-linte": {
            "version": "2.23.0",
            "rating": {
                "III": 12.4
            }
        },
        "vulcanus": {
            "version": "2.23.0",
            "rating": {
                "III": 12.4
            }
        },
        "another-me": {
            "version": "2.23.0",
            "rating": {
                "IV": 12
            }
        },
        "bouquet-colore": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.5,
                "III": 10.3
            }
        },
        "fly-again": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.3
            }
        },
        "galaxy-striker": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.3
            }
        },
        "looking-for-stella": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.5
            }
        },
        "add-venturers": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.4
            }
        },
        "awaken-in-ruins": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.4
            }
        },
        "azure-sky": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "fall-in-me": {
            "version": "2.23.0",
            "rating": {
                "IV": 12
            }
        },
        "higher": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.1
            }
        },
        "love-splash": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.1
            }
        },
        "nee-nee-nee": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "sakura-rain": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "secret-planet": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.1
            }
        },
        "unshakable": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.4
            }
        },
        "veil-of-summer": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.6
            }
        },
        "convallaria": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.3
            }
        },
        "ephemeralization": {
            "version": "2.23.0",
            "rating": {
                "III": 12.3,
                "II": 8.9
            }
        },
        "fallin-fallin": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "freys-philosophy": {
            "version": "2.23.0",
            "rating": {
                "III": 12
            }
        },
        "ginevra": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.1
            }
        },
        "incyde": {
            "version": "2.23.0",
            "rating": {
                "III": 12.3
            }
        },
        "anokumene": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "chrysanthemum": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.6
            }
        },
        "dispersion": {
            "version": "2.23.0",
            "rating": {
                "III": 11.7
            }
        },
        "gokusaishoku-no-yutopia": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.2
            }
        },
        "hoshifuruyoru-to-ichirin-no-hana": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.3
            }
        },
        "lonely-departure": {
            "version": "2.23.0",
            "rating": {
                "III": 10.6
            }
        },
        "memories-of-the-past": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "shinde-shimatta-kisetsu-no-kakera": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.2
            }
        },
        "a-city-in-serenity": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.3
            }
        },
        "burn-it-up": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.7
            }
        },
        "fire-of-heart": {
            "version": "2.23.0",
            "rating": {
                "III": 11.9
            }
        },
        "quadruplicity": {
            "version": "2.23.0",
            "rating": {
                "III": 12.1
            }
        },
        "slide-down": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.4
            }
        },
        "stargazer": {
            "version": "2.23.0",
            "rating": {
                "III": 12.3
            }
        },
        "un1te": {
            "version": "2.23.0",
            "rating": {
                "IV": 11
            }
        },
        "xenith": {
            "version": "2.23.0",
            "rating": {
                "III": 10.1
            }
        },
        "clock-paradox": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.7
            }
        },
        "cybernetic-vampire": {
            "version": "2.23.0",
            "rating": {
                "III": 12
            }
        },
        "enchanted-love": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.2
            }
        },
        "how-to-make-otoge-kyoku": {
            "version": "2.23.0",
            "rating": {
                "III": 11.6
            }
        },
        "night-sky": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.6
            }
        },
        "re-waked-from-abyss": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.1,
                "III": 10.8
            }
        },
        "snapdragon": {
            "version": "2.23.0",
            "rating": {
                "IV": 12
            }
        },
        "song-for-sprites": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.3
            }
        },
        "disorder": {
            "version": "2.23.0",
            "rating": {
                "III": 11.6
            }
        },
        "dont-never-around": {
            "version": "2.23.0",
            "rating": {
                "IV": 12
            }
        },
        "estaminet": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.7
            }
        },
        "grand-i-flora": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.6
            }
        },
        "ieo": {
            "version": "2.23.0",
            "rating": {
                "III": 11.6
            }
        },
        "let-you-dive": {
            "version": "2.23.0",
            "rating": {
                "IV": 12
            }
        },
        "love-you-i-imagined": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.2
            }
        },
        "provison": {
            "version": "2.23.0",
            "rating": {
                "IV": 12
            }
        },
        "sterelogue": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "you-n-die": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9,
                "III": 10.5
            }
        },
        "a-turtles-heart": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.6
            }
        },
        "aqua-stars": {
            "version": "2.23.0",
            "rating": {
                "III": 10.7
            }
        },
        "kai": {
            "version": "2.23.0",
            "rating": {
                "III": 11.4
            }
        },
        "lagtrain": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.8
            }
        },
        "look-at-me-forever": {
            "version": "2.23.0",
            "rating": {
                "III": 11.6
            }
        },
        "may": {
            "version": "2.23.0",
            "rating": {
                "III": 11.2
            }
        },
        "no-one-yes-man": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.8
            }
        },
        "reverie": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.5
            }
        },
        "shuen-kara-inochi-o-sukuu": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.1
            }
        },
        "summer-time-memory": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.3
            }
        },
        "ameni-inoriwo": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.8
            }
        },
        "beautiful-days": {
            "version": "2.23.0",
            "rating": {
                "IV": 10.8
            }
        },
        "is-this-real": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.7
            }
        },
        "journey-with-you": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.2
            }
        },
        "lullaby-for-an-android": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.1
            }
        },
        "pupa": {
            "version": "2.23.0",
            "rating": {
                "III": 11.4
            }
        },
        "pure-white-tale-of-serissa": {
            "version": "2.23.0",
            "rating": {
                "IV": 10.8
            }
        },
        "shijima-ni-ureu": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "starlight-traveler": {
            "version": "2.23.0",
            "rating": {
                "III": 11.4
            }
        },
        "the-promised-land": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.7
            }
        },
        "weaver-wanderer": {
            "version": "2.23.0",
            "rating": {
                "III": 11
            }
        },
        "yubikiri-genman-special": {
            "version": "2.23.0",
            "rating": {
                "IV": 10.6
            }
        },
        "yukianesa": {
            "version": "2.23.0",
            "rating": {
                "III": 11.5
            }
        },
        "bystander-knife": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.7
            }
        },
        "converge": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.8
            }
        },
        "eternal-ascent": {
            "version": "2.23.0",
            "rating": {
                "III": 10.4
            }
        },
        "inn3rflame": {
            "version": "2.23.0",
            "rating": {
                "III": 11.7
            }
        },
        "musaishiki-no-yutopia": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "ninja-ish": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.8
            }
        },
        "sweet-dreams": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.8
            }
        },
        "the-vampire": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.1
            }
        },
        "triad-of-dryad": {
            "version": "2.23.0",
            "rating": {
                "III": 11.9
            }
        },
        "vs-treamer": {
            "version": "2.23.0",
            "rating": {
                "III": 12.2
            }
        },
        "a-clock": {
            "version": "2.23.0",
            "rating": {
                "IV": 10.8
            }
        },
        "anthem": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.7,
                "III": 10.5
            }
        },
        "apocalypse": {
            "version": "2.23.0",
            "rating": {
                "IV": 12
            }
        },
        "break-over": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.8
            }
        },
        "dance-of-the-tiny-dreamer": {
            "version": "2.23.0",
            "rating": {
                "III": 11.5
            }
        },
        "eternal-calm": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.2
            }
        },
        "huggy-wuggy": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.7,
                "III": 10.4
            }
        },
        "ice-festival": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.7
            }
        },
        "igallta": {
            "version": "2.23.0",
            "rating": {
                "III": 11.3
            }
        },
        "k-moe-vip": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.1,
                "III": 10.7
            }
        },
        "monitoring": {
            "version": "2.23.0",
            "rating": {
                "III": 10.5
            }
        },
        "mvurbd": {
            "version": "2.23.0",
            "rating": {
                "III": 11.7
            }
        },
        "phantom": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.3
            }
        },
        "quon": {
            "version": "2.23.0",
            "rating": {
                "III": 11.3
            }
        },
        "revocate": {
            "version": "2.23.0",
            "rating": {
                "III": 10.4
            }
        },
        "witches-party": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.2
            }
        },
        "aorist-hallucination": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.6
            }
        },
        "commotion": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "epitaxy": {
            "version": "2.23.0",
            "rating": {
                "III": 11.4
            }
        },
        "irony": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.6
            }
        },
        "king": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.8
            }
        },
        "make-up-your-world": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.9
            }
        },
        "mendokusai-modo": {
            "version": "2.23.0",
            "rating": {
                "III": 11.7
            }
        },
        "quattuorux": {
            "version": "2.23.0",
            "rating": {
                "III": 10.4
            }
        },
        "shooting-stars": {
            "version": "2.23.0",
            "rating": {
                "III": 10.9
            }
        },
        "wildcard": {
            "version": "2.23.0",
            "rating": {
                "IV": 12.5
            }
        },
        "edge-of-bravery": {
            "version": "2.23.0",
            "rating": {
                "III": 11.4
            }
        },
        "hyp3rtribe": {
            "version": "2.23.0",
            "rating": {
                "III": 10.4
            }
        },
        "indelible-yore": {
            "version": "2.23.0",
            "rating": {
                "III": 10.6
            }
        },
        "infinity-heaven": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.5
            }
        },
        "last-paradise": {
            "version": "2.23.0",
            "rating": {
                "IV": 11
            }
        },
        "psalms": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.3
            }
        },
        "the-endless-for-traveler": {
            "version": "2.23.0",
            "rating": {
                "III": 11.3
            }
        },
        "a-time-for-everything": {
            "version": "2.23.0",
            "rating": {
                "IV": 10.2
            }
        },
        "eschatology": {
            "version": "2.23.0",
            "rating": {
                "III": 11.3
            }
        },
        "excez": {
            "version": "2.23.0",
            "rating": {
                "III": 11.3
            }
        },
        "flashback-flicker": {
            "version": "2.23.0",
            "rating": {
                "III": 11.4
            }
        },
        "one-percent-love": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.5
            }
        },
        "red-bullet": {
            "version": "2.23.0",
            "rating": {
                "III": 10.2
            }
        },
        "torikororu-suteppu": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.2
            }
        },
        "giselle": {
            "version": "2.23.0",
            "rating": {
                "III": 10.9
            }
        },
        "obsidian": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.5
            }
        },
        "ouverture": {
            "version": "2.23.0",
            "rating": {
                "III": 11.4
            }
        },
        "silentphobia": {
            "version": "2.23.0",
            "rating": {
                "III": 11.4
            }
        },
        "snowblind": {
            "version": "2.23.0",
            "rating": {
                "III": 11.1
            }
        },
        "song-for-again": {
            "version": "2.23.0",
            "rating": {
                "IV": 10.3
            }
        },
        "spooky-dance-party": {
            "version": "2.23.0",
            "rating": {
                "III": 11.6
            }
        },
        "star-cape": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.6
            }
        },
        "swirling-blue": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.6
            }
        },
        "sword-of-convallaria": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.1
            }
        },
        "forward-motion": {
            "version": "2.23.0",
            "rating": {
                "III": 10.1
            }
        },
        "after-rain": {
            "version": "2.23.0",
            "rating": {
                "IV": 10.8
            }
        },
        "amethyst": {
            "version": "2.23.0",
            "rating": {
                "III": 10.4
            }
        },
        "autumn-breeze": {
            "version": "2.23.0",
            "rating": {
                "IV": 9
            }
        },
        "velocity": {
            "version": "2.23.0",
            "rating": {
                "IV": 11.3
            }
        },
        "cthugha": {
            "version": "2.23.0",
            "rating": {
                "III": 10.2
            }
        },
        "lost-puppet": {
            "version": "2.23.0",
            "rating": {
                "IV": 10.8
            }
        },
        "today-is-not-tomorrow": {
            "version": "2.23.0",
            "rating": {
                "IV": 11
            }
        },
        "the-amazing-race": {
            "version": "2.23.0",
            "rating": {
                "III": 10.3
            }
        },
        "lost-in-farside": {
            "version": "2.23.0",
            "rating": {
                "III": 10.2
            }
        },
        "dear-my-memories": {
            "version": "2.23.0",
            "rating": {
                "III": 10
            }
        },
        "wakare-no-jokyoku": {
            "version": "2.23.0",
            "rating": {
                "IV": 9
            }
        }
    }
    CHANGE_SONGS = {song_id: {**data, "version": packaging.version.Version(data["version"])} for song_id, data in _CHANGE_SONGS.items()}