import itertools
from copy import deepcopy
import re
from typing import Tuple, List, Optional, Dict, Union, Any

unicode_dict = {
    "Basic Latin[g]": {
        "start": 0,
        "end": 127,
        "code_points": 128,
        "assigned_characters": 128,
        "description": "Latin (52 characters), Common (76 characters)",
    },
    "Latin-1 Supplement[h]": {
        "start": 128,
        "end": 255,
        "code_points": 128,
        "assigned_characters": 128,
        "description": "Latin (64 characters), Common (64 characters)",
    },
    "Latin Extended-A": {
        "start": 256,
        "end": 383,
        "code_points": 128,
        "assigned_characters": 128,
        "description": "Latin",
    },
    "Latin Extended-B": {
        "start": 384,
        "end": 591,
        "code_points": 208,
        "assigned_characters": 208,
        "description": "Latin",
    },
    "IPA Extensions": {
        "start": 592,
        "end": 687,
        "code_points": 96,
        "assigned_characters": 96,
        "description": "Latin",
    },
    "Spacing Modifier Letters": {
        "start": 688,
        "end": 767,
        "code_points": 80,
        "assigned_characters": 80,
        "description": "Bopomofo (2 characters), Latin (14 characters), Common (64 characters)",
    },
    "Combining Diacritical Marks": {
        "start": 768,
        "end": 879,
        "code_points": 112,
        "assigned_characters": 112,
        "description": "Inherited",
    },
    "Greek and Coptic": {
        "start": 880,
        "end": 1023,
        "code_points": 144,
        "assigned_characters": 135,
        "description": "Coptic (14 characters), Greek (117 characters), Common (4 characters)",
    },
    "Cyrillic": {
        "start": 1024,
        "end": 1279,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Cyrillic (254 characters), Inherited (2 characters)",
    },
    "Cyrillic Supplement": {
        "start": 1280,
        "end": 1327,
        "code_points": 48,
        "assigned_characters": 48,
        "description": "Cyrillic",
    },
    "Armenian": {
        "start": 1328,
        "end": 1423,
        "code_points": 96,
        "assigned_characters": 91,
        "description": "Armenian",
    },
    "Hebrew": {
        "start": 1424,
        "end": 1535,
        "code_points": 112,
        "assigned_characters": 88,
        "description": "Hebrew",
    },
    "Arabic": {
        "start": 1536,
        "end": 1791,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Arabic (238 characters), Common (6 characters), Inherited (12 characters)",
    },
    "Syriac": {
        "start": 1792,
        "end": 1871,
        "code_points": 80,
        "assigned_characters": 77,
        "description": "Syriac",
    },
    "Arabic Supplement": {
        "start": 1872,
        "end": 1919,
        "code_points": 48,
        "assigned_characters": 48,
        "description": "Arabic",
    },
    "Thaana": {
        "start": 1920,
        "end": 1983,
        "code_points": 64,
        "assigned_characters": 50,
        "description": "Thaana",
    },
    "NKo": {
        "start": 1984,
        "end": 2047,
        "code_points": 64,
        "assigned_characters": 62,
        "description": "Nko",
    },
    "Samaritan": {
        "start": 2048,
        "end": 2111,
        "code_points": 64,
        "assigned_characters": 61,
        "description": "Samaritan",
    },
    "Mandaic": {
        "start": 2112,
        "end": 2143,
        "code_points": 32,
        "assigned_characters": 29,
        "description": "Mandaic",
    },
    "Syriac Supplement": {
        "start": 2144,
        "end": 2159,
        "code_points": 16,
        "assigned_characters": 11,
        "description": "Syriac",
    },
    "Arabic Extended-B": {
        "start": 2160,
        "end": 2207,
        "code_points": 48,
        "assigned_characters": 41,
        "description": "Arabic",
    },
    "Arabic Extended-A": {
        "start": 2208,
        "end": 2303,
        "code_points": 96,
        "assigned_characters": 96,
        "description": "Arabic (95 characters), Common (1 character)",
    },
    "Devanagari": {
        "start": 2304,
        "end": 2431,
        "code_points": 128,
        "assigned_characters": 128,
        "description": "Devanagari (122 characters), Common (2 characters), Inherited (4 characters)",
    },
    "Bengali": {
        "start": 2432,
        "end": 2559,
        "code_points": 128,
        "assigned_characters": 96,
        "description": "Bengali",
    },
    "Gurmukhi": {
        "start": 2560,
        "end": 2687,
        "code_points": 128,
        "assigned_characters": 80,
        "description": "Gurmukhi",
    },
    "Gujarati": {
        "start": 2688,
        "end": 2815,
        "code_points": 128,
        "assigned_characters": 91,
        "description": "Gujarati",
    },
    "Oriya": {
        "start": 2816,
        "end": 2943,
        "code_points": 128,
        "assigned_characters": 91,
        "description": "Oriya",
    },
    "Tamil": {
        "start": 2944,
        "end": 3071,
        "code_points": 128,
        "assigned_characters": 72,
        "description": "Tamil",
    },
    "Telugu": {
        "start": 3072,
        "end": 3199,
        "code_points": 128,
        "assigned_characters": 100,
        "description": "Telugu",
    },
    "Kannada": {
        "start": 3200,
        "end": 3327,
        "code_points": 128,
        "assigned_characters": 91,
        "description": "Kannada",
    },
    "Malayalam": {
        "start": 3328,
        "end": 3455,
        "code_points": 128,
        "assigned_characters": 118,
        "description": "Malayalam",
    },
    "Sinhala": {
        "start": 3456,
        "end": 3583,
        "code_points": 128,
        "assigned_characters": 91,
        "description": "Sinhala",
    },
    "Thai": {
        "start": 3584,
        "end": 3711,
        "code_points": 128,
        "assigned_characters": 87,
        "description": "Thai (86 characters), Common (1 character)",
    },
    "Lao": {
        "start": 3712,
        "end": 3839,
        "code_points": 128,
        "assigned_characters": 83,
        "description": "Lao",
    },
    "Tibetan": {
        "start": 3840,
        "end": 4095,
        "code_points": 256,
        "assigned_characters": 211,
        "description": "Tibetan (207 characters), Common (4 characters)",
    },
    "Myanmar": {
        "start": 4096,
        "end": 4255,
        "code_points": 160,
        "assigned_characters": 160,
        "description": "Myanmar",
    },
    "Georgian": {
        "start": 4256,
        "end": 4351,
        "code_points": 96,
        "assigned_characters": 88,
        "description": "Georgian (87 characters), Common (1 character)",
    },
    "Hangul Jamo": {
        "start": 4352,
        "end": 4607,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Hangul",
    },
    "Ethiopic": {
        "start": 4608,
        "end": 4991,
        "code_points": 384,
        "assigned_characters": 358,
        "description": "Ethiopic",
    },
    "Ethiopic Supplement": {
        "start": 4992,
        "end": 5023,
        "code_points": 32,
        "assigned_characters": 26,
        "description": "Ethiopic",
    },
    "Cherokee": {
        "start": 5024,
        "end": 5119,
        "code_points": 96,
        "assigned_characters": 92,
        "description": "Cherokee",
    },
    "Unified Canadian Aboriginal Syllabics": {
        "start": 5120,
        "end": 5759,
        "code_points": 640,
        "assigned_characters": 640,
        "description": "Canadian Aboriginal",
    },
    "Ogham": {
        "start": 5760,
        "end": 5791,
        "code_points": 32,
        "assigned_characters": 29,
        "description": "Ogham",
    },
    "Runic": {
        "start": 5792,
        "end": 5887,
        "code_points": 96,
        "assigned_characters": 89,
        "description": "Runic (86 characters), Common (3 characters)",
    },
    "Tagalog": {
        "start": 5888,
        "end": 5919,
        "code_points": 32,
        "assigned_characters": 23,
        "description": "Tagalog",
    },
    "Hanunoo": {
        "start": 5920,
        "end": 5951,
        "code_points": 32,
        "assigned_characters": 23,
        "description": "Hanunoo (21 characters), Common (2 characters)",
    },
    "Buhid": {
        "start": 5952,
        "end": 5983,
        "code_points": 32,
        "assigned_characters": 20,
        "description": "Buhid",
    },
    "Tagbanwa": {
        "start": 5984,
        "end": 6015,
        "code_points": 32,
        "assigned_characters": 18,
        "description": "Tagbanwa",
    },
    "Khmer": {
        "start": 6016,
        "end": 6143,
        "code_points": 128,
        "assigned_characters": 114,
        "description": "Khmer",
    },
    "Mongolian": {
        "start": 6144,
        "end": 6319,
        "code_points": 176,
        "assigned_characters": 158,
        "description": "Mongolian (155 characters), Common (3 characters)",
    },
    "Unified Canadian Aboriginal Syllabics Extended": {
        "start": 6320,
        "end": 6399,
        "code_points": 80,
        "assigned_characters": 70,
        "description": "Canadian Aboriginal",
    },
    "Limbu": {
        "start": 6400,
        "end": 6479,
        "code_points": 80,
        "assigned_characters": 68,
        "description": "Limbu",
    },
    "Tai Le": {
        "start": 6480,
        "end": 6527,
        "code_points": 48,
        "assigned_characters": 35,
        "description": "Tai Le",
    },
    "New Tai Lue": {
        "start": 6528,
        "end": 6623,
        "code_points": 96,
        "assigned_characters": 83,
        "description": "New Tai Lue",
    },
    "Khmer Symbols": {
        "start": 6624,
        "end": 6655,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Khmer",
    },
    "Buginese": {
        "start": 6656,
        "end": 6687,
        "code_points": 32,
        "assigned_characters": 30,
        "description": "Buginese",
    },
    "Tai Tham": {
        "start": 6688,
        "end": 6831,
        "code_points": 144,
        "assigned_characters": 127,
        "description": "Tai Tham",
    },
    "Combining Diacritical Marks Extended": {
        "start": 6832,
        "end": 6911,
        "code_points": 80,
        "assigned_characters": 31,
        "description": "Inherited",
    },
    "Balinese": {
        "start": 6912,
        "end": 7039,
        "code_points": 128,
        "assigned_characters": 124,
        "description": "Balinese",
    },
    "Sundanese": {
        "start": 7040,
        "end": 7103,
        "code_points": 64,
        "assigned_characters": 64,
        "description": "Sundanese",
    },
    "Batak": {
        "start": 7104,
        "end": 7167,
        "code_points": 64,
        "assigned_characters": 56,
        "description": "Batak",
    },
    "Lepcha": {
        "start": 7168,
        "end": 7247,
        "code_points": 80,
        "assigned_characters": 74,
        "description": "Lepcha",
    },
    "Ol Chiki": {
        "start": 7248,
        "end": 7295,
        "code_points": 48,
        "assigned_characters": 48,
        "description": "Ol Chiki",
    },
    "Cyrillic Extended-C": {
        "start": 7296,
        "end": 7311,
        "code_points": 16,
        "assigned_characters": 9,
        "description": "Cyrillic",
    },
    "Georgian Extended": {
        "start": 7312,
        "end": 7359,
        "code_points": 48,
        "assigned_characters": 46,
        "description": "Georgian",
    },
    "Sundanese Supplement": {
        "start": 7360,
        "end": 7375,
        "code_points": 16,
        "assigned_characters": 8,
        "description": "Sundanese",
    },
    "Vedic Extensions": {
        "start": 7376,
        "end": 7423,
        "code_points": 48,
        "assigned_characters": 43,
        "description": "Common (16 characters), Inherited (27 characters)",
    },
    "Phonetic Extensions": {
        "start": 7424,
        "end": 7551,
        "code_points": 128,
        "assigned_characters": 128,
        "description": "Cyrillic (2 characters), Greek (15 characters), Latin (111 characters)",
    },
    "Phonetic Extensions Supplement": {
        "start": 7552,
        "end": 7615,
        "code_points": 64,
        "assigned_characters": 64,
        "description": "Greek (1 character), Latin (63 characters)",
    },
    "Combining Diacritical Marks Supplement": {
        "start": 7616,
        "end": 7679,
        "code_points": 64,
        "assigned_characters": 64,
        "description": "Inherited",
    },
    "Latin Extended Additional": {
        "start": 7680,
        "end": 7935,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Latin",
    },
    "Greek Extended": {
        "start": 7936,
        "end": 8191,
        "code_points": 256,
        "assigned_characters": 233,
        "description": "Greek",
    },
    "General Punctuation": {
        "start": 8192,
        "end": 8303,
        "code_points": 112,
        "assigned_characters": 111,
        "description": "Common (109 characters), Inherited (2 characters)",
    },
    "Superscripts and Subscripts": {
        "start": 8304,
        "end": 8351,
        "code_points": 48,
        "assigned_characters": 42,
        "description": "Latin (15 characters), Common (27 characters)",
    },
    "Currency Symbols": {
        "start": 8352,
        "end": 8399,
        "code_points": 48,
        "assigned_characters": 33,
        "description": "Common",
    },
    "Combining Diacritical Marks for Symbols": {
        "start": 8400,
        "end": 8447,
        "code_points": 48,
        "assigned_characters": 33,
        "description": "Inherited",
    },
    "Letterlike Symbols": {
        "start": 8448,
        "end": 8527,
        "code_points": 80,
        "assigned_characters": 80,
        "description": "Greek (1 character), Latin (4 characters), Common (75 characters)",
    },
    "Number Forms": {
        "start": 8528,
        "end": 8591,
        "code_points": 64,
        "assigned_characters": 60,
        "description": "Latin (41 characters), Common (19 characters)",
    },
    "Arrows": {
        "start": 8592,
        "end": 8703,
        "code_points": 112,
        "assigned_characters": 112,
        "description": "Common",
    },
    "Mathematical Operators": {
        "start": 8704,
        "end": 8959,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Common",
    },
    "Miscellaneous Technical": {
        "start": 8960,
        "end": 9215,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Common",
    },
    "Control Pictures": {
        "start": 9216,
        "end": 9279,
        "code_points": 64,
        "assigned_characters": 39,
        "description": "Common",
    },
    "Optical Character Recognition": {
        "start": 9280,
        "end": 9311,
        "code_points": 32,
        "assigned_characters": 11,
        "description": "Common",
    },
    "Enclosed Alphanumerics": {
        "start": 9312,
        "end": 9471,
        "code_points": 160,
        "assigned_characters": 160,
        "description": "Common",
    },
    "Box Drawing": {
        "start": 9472,
        "end": 9599,
        "code_points": 128,
        "assigned_characters": 128,
        "description": "Common",
    },
    "Block Elements": {
        "start": 9600,
        "end": 9631,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Common",
    },
    "Geometric Shapes": {
        "start": 9632,
        "end": 9727,
        "code_points": 96,
        "assigned_characters": 96,
        "description": "Common",
    },
    "Miscellaneous Symbols": {
        "start": 9728,
        "end": 9983,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Common",
    },
    "Dingbats": {
        "start": 9984,
        "end": 10175,
        "code_points": 192,
        "assigned_characters": 192,
        "description": "Common",
    },
    "Miscellaneous Mathematical Symbols-A": {
        "start": 10176,
        "end": 10223,
        "code_points": 48,
        "assigned_characters": 48,
        "description": "Common",
    },
    "Supplemental Arrows-A": {
        "start": 10224,
        "end": 10239,
        "code_points": 16,
        "assigned_characters": 16,
        "description": "Common",
    },
    "Braille Patterns": {
        "start": 10240,
        "end": 10495,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Braille",
    },
    "Supplemental Arrows-B": {
        "start": 10496,
        "end": 10623,
        "code_points": 128,
        "assigned_characters": 128,
        "description": "Common",
    },
    "Miscellaneous Mathematical Symbols-B": {
        "start": 10624,
        "end": 10751,
        "code_points": 128,
        "assigned_characters": 128,
        "description": "Common",
    },
    "Supplemental Mathematical Operators": {
        "start": 10752,
        "end": 11007,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Common",
    },
    "Miscellaneous Symbols and Arrows": {
        "start": 11008,
        "end": 11263,
        "code_points": 256,
        "assigned_characters": 253,
        "description": "Common",
    },
    "Glagolitic": {
        "start": 11264,
        "end": 11359,
        "code_points": 96,
        "assigned_characters": 96,
        "description": "Glagolitic",
    },
    "Latin Extended-C": {
        "start": 11360,
        "end": 11391,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Latin",
    },
    "Coptic": {
        "start": 11392,
        "end": 11519,
        "code_points": 128,
        "assigned_characters": 123,
        "description": "Coptic",
    },
    "Georgian Supplement": {
        "start": 11520,
        "end": 11567,
        "code_points": 48,
        "assigned_characters": 40,
        "description": "Georgian",
    },
    "Tifinagh": {
        "start": 11568,
        "end": 11647,
        "code_points": 80,
        "assigned_characters": 59,
        "description": "Tifinagh",
    },
    "Ethiopic Extended": {
        "start": 11648,
        "end": 11743,
        "code_points": 96,
        "assigned_characters": 79,
        "description": "Ethiopic",
    },
    "Cyrillic Extended-A": {
        "start": 11744,
        "end": 11775,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Cyrillic",
    },
    "Supplemental Punctuation": {
        "start": 11776,
        "end": 11903,
        "code_points": 128,
        "assigned_characters": 94,
        "description": "Common",
    },
    "CJK Radicals Supplement": {
        "start": 11904,
        "end": 12031,
        "code_points": 128,
        "assigned_characters": 115,
        "description": "Han",
    },
    "Kangxi Radicals": {
        "start": 12032,
        "end": 12255,
        "code_points": 224,
        "assigned_characters": 214,
        "description": "Han",
    },
    "Ideographic Description Characters": {
        "start": 12272,
        "end": 12287,
        "code_points": 16,
        "assigned_characters": 16,
        "description": "Common",
    },
    "CJK Symbols and Punctuation": {
        "start": 12288,
        "end": 12351,
        "code_points": 64,
        "assigned_characters": 64,
        "description": "Han (15 characters), Hangul (2 characters), Common (43 characters), Inherited (4 characters)",
    },
    "Hiragana": {
        "start": 12352,
        "end": 12447,
        "code_points": 96,
        "assigned_characters": 93,
        "description": "Hiragana (89 characters), Common (2 characters), Inherited (2 characters)",
    },
    "Katakana": {
        "start": 12448,
        "end": 12543,
        "code_points": 96,
        "assigned_characters": 96,
        "description": "Katakana (93 characters), Common (3 characters)",
    },
    "Bopomofo": {
        "start": 12544,
        "end": 12591,
        "code_points": 48,
        "assigned_characters": 43,
        "description": "Bopomofo",
    },
    "Hangul Compatibility Jamo": {
        "start": 12592,
        "end": 12687,
        "code_points": 96,
        "assigned_characters": 94,
        "description": "Hangul",
    },
    "Kanbun": {
        "start": 12688,
        "end": 12703,
        "code_points": 16,
        "assigned_characters": 16,
        "description": "Common",
    },
    "Bopomofo Extended": {
        "start": 12704,
        "end": 12735,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Bopomofo",
    },
    "CJK Strokes": {
        "start": 12736,
        "end": 12783,
        "code_points": 48,
        "assigned_characters": 37,
        "description": "Common",
    },
    "Katakana Phonetic Extensions": {
        "start": 12784,
        "end": 12799,
        "code_points": 16,
        "assigned_characters": 16,
        "description": "Katakana",
    },
    "Enclosed CJK Letters and Months": {
        "start": 12800,
        "end": 13055,
        "code_points": 256,
        "assigned_characters": 255,
        "description": "Hangul (62 characters), Katakana (47 characters), Common (146 characters)",
    },
    "CJK Compatibility": {
        "start": 13056,
        "end": 13311,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Katakana (88 characters), Common (168 characters)",
    },
    "CJK Unified Ideographs Extension A": {
        "start": 13312,
        "end": 19903,
        "code_points": 6592,
        "assigned_characters": 6592,
        "description": "Han",
    },
    "Yijing Hexagram Symbols": {
        "start": 19904,
        "end": 19967,
        "code_points": 64,
        "assigned_characters": 64,
        "description": "Common",
    },
    "CJK Unified Ideographs": {
        "start": 19968,
        "end": 40959,
        "code_points": 20992,
        "assigned_characters": 20992,
        "description": "Han",
    },
    "Yi Syllables": {
        "start": 40960,
        "end": 42127,
        "code_points": 1168,
        "assigned_characters": 1165,
        "description": "Yi",
    },
    "Yi Radicals": {
        "start": 42128,
        "end": 42191,
        "code_points": 64,
        "assigned_characters": 55,
        "description": "Yi",
    },
    "Lisu": {
        "start": 42192,
        "end": 42239,
        "code_points": 48,
        "assigned_characters": 48,
        "description": "Lisu",
    },
    "Vai": {
        "start": 42240,
        "end": 42559,
        "code_points": 320,
        "assigned_characters": 300,
        "description": "Vai",
    },
    "Cyrillic Extended-B": {
        "start": 42560,
        "end": 42655,
        "code_points": 96,
        "assigned_characters": 96,
        "description": "Cyrillic",
    },
    "Bamum": {
        "start": 42656,
        "end": 42751,
        "code_points": 96,
        "assigned_characters": 88,
        "description": "Bamum",
    },
    "Modifier Tone Letters": {
        "start": 42752,
        "end": 42783,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Common",
    },
    "Latin Extended-D": {
        "start": 42784,
        "end": 43007,
        "code_points": 224,
        "assigned_characters": 193,
        "description": "Latin (188 characters), Common (5 characters)",
    },
    "Syloti Nagri": {
        "start": 43008,
        "end": 43055,
        "code_points": 48,
        "assigned_characters": 45,
        "description": "Syloti Nagri",
    },
    "Common Indic Number Forms": {
        "start": 43056,
        "end": 43071,
        "code_points": 16,
        "assigned_characters": 10,
        "description": "Common",
    },
    "Phags-pa": {
        "start": 43072,
        "end": 43135,
        "code_points": 64,
        "assigned_characters": 56,
        "description": "Phags Pa",
    },
    "Saurashtra": {
        "start": 43136,
        "end": 43231,
        "code_points": 96,
        "assigned_characters": 82,
        "description": "Saurashtra",
    },
    "Devanagari Extended": {
        "start": 43232,
        "end": 43263,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Devanagari",
    },
    "Kayah Li": {
        "start": 43264,
        "end": 43311,
        "code_points": 48,
        "assigned_characters": 48,
        "description": "Kayah Li (47 characters), Common (1 character)",
    },
    "Rejang": {
        "start": 43312,
        "end": 43359,
        "code_points": 48,
        "assigned_characters": 37,
        "description": "Rejang",
    },
    "Hangul Jamo Extended-A": {
        "start": 43360,
        "end": 43391,
        "code_points": 32,
        "assigned_characters": 29,
        "description": "Hangul",
    },
    "Javanese": {
        "start": 43392,
        "end": 43487,
        "code_points": 96,
        "assigned_characters": 91,
        "description": "Javanese (90 characters), Common (1 character)",
    },
    "Myanmar Extended-B": {
        "start": 43488,
        "end": 43519,
        "code_points": 32,
        "assigned_characters": 31,
        "description": "Myanmar",
    },
    "Cham": {
        "start": 43520,
        "end": 43615,
        "code_points": 96,
        "assigned_characters": 83,
        "description": "Cham",
    },
    "Myanmar Extended-A": {
        "start": 43616,
        "end": 43647,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Myanmar",
    },
    "Tai Viet": {
        "start": 43648,
        "end": 43743,
        "code_points": 96,
        "assigned_characters": 72,
        "description": "Tai Viet",
    },
    "Meetei Mayek Extensions": {
        "start": 43744,
        "end": 43775,
        "code_points": 32,
        "assigned_characters": 23,
        "description": "Meetei Mayek",
    },
    "Ethiopic Extended-A": {
        "start": 43776,
        "end": 43823,
        "code_points": 48,
        "assigned_characters": 32,
        "description": "Ethiopic",
    },
    "Latin Extended-E": {
        "start": 43824,
        "end": 43887,
        "code_points": 64,
        "assigned_characters": 60,
        "description": "Latin (56 characters), Greek (1 character), Common (3 characters)",
    },
    "Cherokee Supplement": {
        "start": 43888,
        "end": 43967,
        "code_points": 80,
        "assigned_characters": 80,
        "description": "Cherokee",
    },
    "Meetei Mayek": {
        "start": 43968,
        "end": 44031,
        "code_points": 64,
        "assigned_characters": 56,
        "description": "Meetei Mayek",
    },
    "Hangul Syllables": {
        "start": 44032,
        "end": 55215,
        "code_points": 11184,
        "assigned_characters": 11172,
        "description": "Hangul",
    },
    "Hangul Jamo Extended-B": {
        "start": 55216,
        "end": 55295,
        "code_points": 80,
        "assigned_characters": 72,
        "description": "Hangul",
    },
    "High Surrogates": {
        "start": 55296,
        "end": 56191,
        "code_points": 896,
        "assigned_characters": 0,
        "description": "Unknown",
    },
    "High Private Use Surrogates": {
        "start": 56192,
        "end": 56319,
        "code_points": 128,
        "assigned_characters": 0,
        "description": "Unknown",
    },
    "Low Surrogates": {
        "start": 56320,
        "end": 57343,
        "code_points": 1024,
        "assigned_characters": 0,
        "description": "Unknown",
    },
    "Private Use Area": {
        "start": 57344,
        "end": 63743,
        "code_points": 6400,
        "assigned_characters": 6400,
        "description": "Unknown",
    },
    "CJK Compatibility Ideographs": {
        "start": 63744,
        "end": 64255,
        "code_points": 512,
        "assigned_characters": 472,
        "description": "Han",
    },
    "Alphabetic Presentation Forms": {
        "start": 64256,
        "end": 64335,
        "code_points": 80,
        "assigned_characters": 58,
        "description": "Armenian (5 characters), Hebrew (46 characters), Latin (7 characters)",
    },
    "Arabic Presentation Forms-A": {
        "start": 64336,
        "end": 65023,
        "code_points": 688,
        "assigned_characters": 631,
        "description": "Arabic (629 characters), Common (2 characters)",
    },
    "Variation Selectors": {
        "start": 65024,
        "end": 65039,
        "code_points": 16,
        "assigned_characters": 16,
        "description": "Inherited",
    },
    "Vertical Forms": {
        "start": 65040,
        "end": 65055,
        "code_points": 16,
        "assigned_characters": 10,
        "description": "Common",
    },
    "Combining Half Marks": {
        "start": 65056,
        "end": 65071,
        "code_points": 16,
        "assigned_characters": 16,
        "description": "Cyrillic (2 characters), Inherited (14 characters)",
    },
    "CJK Compatibility Forms": {
        "start": 65072,
        "end": 65103,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Common",
    },
    "Small Form Variants": {
        "start": 65104,
        "end": 65135,
        "code_points": 32,
        "assigned_characters": 26,
        "description": "Common",
    },
    "Arabic Presentation Forms-B": {
        "start": 65136,
        "end": 65279,
        "code_points": 144,
        "assigned_characters": 141,
        "description": "Arabic (140 characters), Common (1 character)",
    },
    "Halfwidth and Fullwidth Forms": {
        "start": 65280,
        "end": 65519,
        "code_points": 240,
        "assigned_characters": 225,
        "description": "Hangul (52 characters), Katakana (55 characters), Latin (52 characters), Common (66 characters)",
    },
    "Specials": {
        "start": 65520,
        "end": 65535,
        "code_points": 16,
        "assigned_characters": 5,
        "description": "Common",
    },
    "Linear B Syllabary": {
        "start": 65536,
        "end": 65663,
        "code_points": 128,
        "assigned_characters": 88,
        "description": "Linear B",
    },
    "Linear B Ideograms": {
        "start": 65664,
        "end": 65791,
        "code_points": 128,
        "assigned_characters": 123,
        "description": "Linear B",
    },
    "Aegean Numbers": {
        "start": 65792,
        "end": 65855,
        "code_points": 64,
        "assigned_characters": 57,
        "description": "Common",
    },
    "Ancient Greek Numbers": {
        "start": 65856,
        "end": 65935,
        "code_points": 80,
        "assigned_characters": 79,
        "description": "Greek",
    },
    "Ancient Symbols": {
        "start": 65936,
        "end": 65999,
        "code_points": 64,
        "assigned_characters": 14,
        "description": "Greek (1 character), Common (13 characters)",
    },
    "Phaistos Disc": {
        "start": 66000,
        "end": 66047,
        "code_points": 48,
        "assigned_characters": 46,
        "description": "Common (45 characters), Inherited (1 character)",
    },
    "Lycian": {
        "start": 66176,
        "end": 66207,
        "code_points": 32,
        "assigned_characters": 29,
        "description": "Lycian",
    },
    "Carian": {
        "start": 66208,
        "end": 66271,
        "code_points": 64,
        "assigned_characters": 49,
        "description": "Carian",
    },
    "Coptic Epact Numbers": {
        "start": 66272,
        "end": 66303,
        "code_points": 32,
        "assigned_characters": 28,
        "description": "Common (27 characters), Inherited (1 character)",
    },
    "Old Italic": {
        "start": 66304,
        "end": 66351,
        "code_points": 48,
        "assigned_characters": 39,
        "description": "Old Italic",
    },
    "Gothic": {
        "start": 66352,
        "end": 66383,
        "code_points": 32,
        "assigned_characters": 27,
        "description": "Gothic",
    },
    "Old Permic": {
        "start": 66384,
        "end": 66431,
        "code_points": 48,
        "assigned_characters": 43,
        "description": "Old Permic",
    },
    "Ugaritic": {
        "start": 66432,
        "end": 66463,
        "code_points": 32,
        "assigned_characters": 31,
        "description": "Ugaritic",
    },
    "Old Persian": {
        "start": 66464,
        "end": 66527,
        "code_points": 64,
        "assigned_characters": 50,
        "description": "Old Persian",
    },
    "Deseret": {
        "start": 66560,
        "end": 66639,
        "code_points": 80,
        "assigned_characters": 80,
        "description": "Deseret",
    },
    "Shavian": {
        "start": 66640,
        "end": 66687,
        "code_points": 48,
        "assigned_characters": 48,
        "description": "Shavian",
    },
    "Osmanya": {
        "start": 66688,
        "end": 66735,
        "code_points": 48,
        "assigned_characters": 40,
        "description": "Osmanya",
    },
    "Osage": {
        "start": 66736,
        "end": 66815,
        "code_points": 80,
        "assigned_characters": 72,
        "description": "Osage",
    },
    "Elbasan": {
        "start": 66816,
        "end": 66863,
        "code_points": 48,
        "assigned_characters": 40,
        "description": "Elbasan",
    },
    "Caucasian Albanian": {
        "start": 66864,
        "end": 66927,
        "code_points": 64,
        "assigned_characters": 53,
        "description": "Caucasian Albanian",
    },
    "Vithkuqi": {
        "start": 66928,
        "end": 67007,
        "code_points": 80,
        "assigned_characters": 70,
        "description": "Vithkuqi",
    },
    "Linear A": {
        "start": 67072,
        "end": 67455,
        "code_points": 384,
        "assigned_characters": 341,
        "description": "Linear A",
    },
    "Latin Extended-F": {
        "start": 67456,
        "end": 67519,
        "code_points": 64,
        "assigned_characters": 57,
        "description": "Latin",
    },
    "Cypriot Syllabary": {
        "start": 67584,
        "end": 67647,
        "code_points": 64,
        "assigned_characters": 55,
        "description": "Cypriot",
    },
    "Imperial Aramaic": {
        "start": 67648,
        "end": 67679,
        "code_points": 32,
        "assigned_characters": 31,
        "description": "Imperial Aramaic",
    },
    "Palmyrene": {
        "start": 67680,
        "end": 67711,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Palmyrene",
    },
    "Nabataean": {
        "start": 67712,
        "end": 67759,
        "code_points": 48,
        "assigned_characters": 40,
        "description": "Nabataean",
    },
    "Hatran": {
        "start": 67808,
        "end": 67839,
        "code_points": 32,
        "assigned_characters": 26,
        "description": "Hatran",
    },
    "Phoenician": {
        "start": 67840,
        "end": 67871,
        "code_points": 32,
        "assigned_characters": 29,
        "description": "Phoenician",
    },
    "Lydian": {
        "start": 67872,
        "end": 67903,
        "code_points": 32,
        "assigned_characters": 27,
        "description": "Lydian",
    },
    "Meroitic Hieroglyphs": {
        "start": 67968,
        "end": 67999,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Meroitic Hieroglyphs",
    },
    "Meroitic Cursive": {
        "start": 68000,
        "end": 68095,
        "code_points": 96,
        "assigned_characters": 90,
        "description": "Meroitic Cursive",
    },
    "Kharoshthi": {
        "start": 68096,
        "end": 68191,
        "code_points": 96,
        "assigned_characters": 68,
        "description": "Kharoshthi",
    },
    "Old South Arabian": {
        "start": 68192,
        "end": 68223,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Old South Arabian",
    },
    "Old North Arabian": {
        "start": 68224,
        "end": 68255,
        "code_points": 32,
        "assigned_characters": 32,
        "description": "Old North Arabian",
    },
    "Manichaean": {
        "start": 68288,
        "end": 68351,
        "code_points": 64,
        "assigned_characters": 51,
        "description": "Manichaean",
    },
    "Avestan": {
        "start": 68352,
        "end": 68415,
        "code_points": 64,
        "assigned_characters": 61,
        "description": "Avestan",
    },
    "Inscriptional Parthian": {
        "start": 68416,
        "end": 68447,
        "code_points": 32,
        "assigned_characters": 30,
        "description": "Inscriptional Parthian",
    },
    "Inscriptional Pahlavi": {
        "start": 68448,
        "end": 68479,
        "code_points": 32,
        "assigned_characters": 27,
        "description": "Inscriptional Pahlavi",
    },
    "Psalter Pahlavi": {
        "start": 68480,
        "end": 68527,
        "code_points": 48,
        "assigned_characters": 29,
        "description": "Psalter Pahlavi",
    },
    "Old Turkic": {
        "start": 68608,
        "end": 68687,
        "code_points": 80,
        "assigned_characters": 73,
        "description": "Old Turkic",
    },
    "Old Hungarian": {
        "start": 68736,
        "end": 68863,
        "code_points": 128,
        "assigned_characters": 108,
        "description": "Old Hungarian",
    },
    "Hanifi Rohingya": {
        "start": 68864,
        "end": 68927,
        "code_points": 64,
        "assigned_characters": 50,
        "description": "Hanifi Rohingya",
    },
    "Rumi Numeral Symbols": {
        "start": 69216,
        "end": 69247,
        "code_points": 32,
        "assigned_characters": 31,
        "description": "Arabic",
    },
    "Yezidi": {
        "start": 69248,
        "end": 69311,
        "code_points": 64,
        "assigned_characters": 47,
        "description": "Yezidi",
    },
    "Arabic Extended-C": {
        "start": 69312,
        "end": 69375,
        "code_points": 64,
        "assigned_characters": 3,
        "description": "Arabic",
    },
    "Old Sogdian": {
        "start": 69376,
        "end": 69423,
        "code_points": 48,
        "assigned_characters": 40,
        "description": "Old Sogdian",
    },
    "Sogdian": {
        "start": 69424,
        "end": 69487,
        "code_points": 64,
        "assigned_characters": 42,
        "description": "Sogdian",
    },
    "Old Uyghur": {
        "start": 69488,
        "end": 69551,
        "code_points": 64,
        "assigned_characters": 26,
        "description": "Old Uyghur",
    },
    "Chorasmian": {
        "start": 69552,
        "end": 69599,
        "code_points": 48,
        "assigned_characters": 28,
        "description": "Chorasmian",
    },
    "Elymaic": {
        "start": 69600,
        "end": 69631,
        "code_points": 32,
        "assigned_characters": 23,
        "description": "Elymaic",
    },
    "Brahmi": {
        "start": 69632,
        "end": 69759,
        "code_points": 128,
        "assigned_characters": 115,
        "description": "Brahmi",
    },
    "Kaithi": {
        "start": 69760,
        "end": 69839,
        "code_points": 80,
        "assigned_characters": 68,
        "description": "Kaithi",
    },
    "Sora Sompeng": {
        "start": 69840,
        "end": 69887,
        "code_points": 48,
        "assigned_characters": 35,
        "description": "Sora Sompeng",
    },
    "Chakma": {
        "start": 69888,
        "end": 69967,
        "code_points": 80,
        "assigned_characters": 71,
        "description": "Chakma",
    },
    "Mahajani": {
        "start": 69968,
        "end": 70015,
        "code_points": 48,
        "assigned_characters": 39,
        "description": "Mahajani",
    },
    "Sharada": {
        "start": 70016,
        "end": 70111,
        "code_points": 96,
        "assigned_characters": 96,
        "description": "Sharada",
    },
    "Sinhala Archaic Numbers": {
        "start": 70112,
        "end": 70143,
        "code_points": 32,
        "assigned_characters": 20,
        "description": "Sinhala",
    },
    "Khojki": {
        "start": 70144,
        "end": 70223,
        "code_points": 80,
        "assigned_characters": 65,
        "description": "Khojki",
    },
    "Multani": {
        "start": 70272,
        "end": 70319,
        "code_points": 48,
        "assigned_characters": 38,
        "description": "Multani",
    },
    "Khudawadi": {
        "start": 70320,
        "end": 70399,
        "code_points": 80,
        "assigned_characters": 69,
        "description": "Khudawadi",
    },
    "Grantha": {
        "start": 70400,
        "end": 70527,
        "code_points": 128,
        "assigned_characters": 86,
        "description": "Grantha (85 characters), Inherited (1 character)",
    },
    "Newa": {
        "start": 70656,
        "end": 70783,
        "code_points": 128,
        "assigned_characters": 97,
        "description": "Newa",
    },
    "Tirhuta": {
        "start": 70784,
        "end": 70879,
        "code_points": 96,
        "assigned_characters": 82,
        "description": "Tirhuta",
    },
    "Siddham": {
        "start": 71040,
        "end": 71167,
        "code_points": 128,
        "assigned_characters": 92,
        "description": "Siddham",
    },
    "Modi": {
        "start": 71168,
        "end": 71263,
        "code_points": 96,
        "assigned_characters": 79,
        "description": "Modi",
    },
    "Mongolian Supplement": {
        "start": 71264,
        "end": 71295,
        "code_points": 32,
        "assigned_characters": 13,
        "description": "Mongolian",
    },
    "Takri": {
        "start": 71296,
        "end": 71375,
        "code_points": 80,
        "assigned_characters": 68,
        "description": "Takri",
    },
    "Ahom": {
        "start": 71424,
        "end": 71503,
        "code_points": 80,
        "assigned_characters": 65,
        "description": "Ahom",
    },
    "Dogra": {
        "start": 71680,
        "end": 71759,
        "code_points": 80,
        "assigned_characters": 60,
        "description": "Dogra",
    },
    "Warang Citi": {
        "start": 71840,
        "end": 71935,
        "code_points": 96,
        "assigned_characters": 84,
        "description": "Warang Citi",
    },
    "Dives Akuru": {
        "start": 71936,
        "end": 72031,
        "code_points": 96,
        "assigned_characters": 72,
        "description": "Dives Akuru",
    },
    "Nandinagari": {
        "start": 72096,
        "end": 72191,
        "code_points": 96,
        "assigned_characters": 65,
        "description": "Nandinagari",
    },
    "Zanabazar Square": {
        "start": 72192,
        "end": 72271,
        "code_points": 80,
        "assigned_characters": 72,
        "description": "Zanabazar Square",
    },
    "Soyombo": {
        "start": 72272,
        "end": 72367,
        "code_points": 96,
        "assigned_characters": 83,
        "description": "Soyombo",
    },
    "Unified Canadian Aboriginal Syllabics Extended-A": {
        "start": 72368,
        "end": 72383,
        "code_points": 16,
        "assigned_characters": 16,
        "description": "Canadian Aboriginal",
    },
    "Pau Cin Hau": {
        "start": 72384,
        "end": 72447,
        "code_points": 64,
        "assigned_characters": 57,
        "description": "Pau Cin Hau",
    },
    "Devanagari Extended-A": {
        "start": 72448,
        "end": 72543,
        "code_points": 96,
        "assigned_characters": 10,
        "description": "Devanagari",
    },
    "Bhaiksuki": {
        "start": 72704,
        "end": 72815,
        "code_points": 112,
        "assigned_characters": 97,
        "description": "Bhaiksuki",
    },
    "Marchen": {
        "start": 72816,
        "end": 72895,
        "code_points": 80,
        "assigned_characters": 68,
        "description": "Marchen",
    },
    "Masaram Gondi": {
        "start": 72960,
        "end": 73055,
        "code_points": 96,
        "assigned_characters": 75,
        "description": "Masaram Gondi",
    },
    "Gunjala Gondi": {
        "start": 73056,
        "end": 73135,
        "code_points": 80,
        "assigned_characters": 63,
        "description": "Gunjala Gondi",
    },
    "Makasar": {
        "start": 73440,
        "end": 73471,
        "code_points": 32,
        "assigned_characters": 25,
        "description": "Makasar",
    },
    "Kawi": {
        "start": 73472,
        "end": 73567,
        "code_points": 96,
        "assigned_characters": 86,
        "description": "Kawi",
    },
    "Lisu Supplement": {
        "start": 73648,
        "end": 73663,
        "code_points": 16,
        "assigned_characters": 1,
        "description": "Lisu",
    },
    "Tamil Supplement": {
        "start": 73664,
        "end": 73727,
        "code_points": 64,
        "assigned_characters": 51,
        "description": "Tamil",
    },
    "Cuneiform": {
        "start": 73728,
        "end": 74751,
        "code_points": 1024,
        "assigned_characters": 922,
        "description": "Cuneiform",
    },
    "Cuneiform Numbers and Punctuation": {
        "start": 74752,
        "end": 74879,
        "code_points": 128,
        "assigned_characters": 116,
        "description": "Cuneiform",
    },
    "Early Dynastic Cuneiform": {
        "start": 74880,
        "end": 75087,
        "code_points": 208,
        "assigned_characters": 196,
        "description": "Cuneiform",
    },
    "Cypro-Minoan": {
        "start": 77712,
        "end": 77823,
        "code_points": 112,
        "assigned_characters": 99,
        "description": "Cypro Minoan",
    },
    "Egyptian Hieroglyphs": {
        "start": 77824,
        "end": 78895,
        "code_points": 1072,
        "assigned_characters": 1072,
        "description": "Egyptian Hieroglyphs",
    },
    "Egyptian Hieroglyph Format Controls": {
        "start": 78896,
        "end": 78943,
        "code_points": 48,
        "assigned_characters": 38,
        "description": "Egyptian Hieroglyphs",
    },
    "Anatolian Hieroglyphs": {
        "start": 82944,
        "end": 83583,
        "code_points": 640,
        "assigned_characters": 583,
        "description": "Anatolian Hieroglyphs",
    },
    "Bamum Supplement": {
        "start": 92160,
        "end": 92735,
        "code_points": 576,
        "assigned_characters": 569,
        "description": "Bamum",
    },
    "Mro": {
        "start": 92736,
        "end": 92783,
        "code_points": 48,
        "assigned_characters": 43,
        "description": "Mro",
    },
    "Tangsa": {
        "start": 92784,
        "end": 92879,
        "code_points": 96,
        "assigned_characters": 89,
        "description": "Tangsa",
    },
    "Bassa Vah": {
        "start": 92880,
        "end": 92927,
        "code_points": 48,
        "assigned_characters": 36,
        "description": "Bassa Vah",
    },
    "Pahawh Hmong": {
        "start": 92928,
        "end": 93071,
        "code_points": 144,
        "assigned_characters": 127,
        "description": "Pahawh Hmong",
    },
    "Medefaidrin": {
        "start": 93760,
        "end": 93855,
        "code_points": 96,
        "assigned_characters": 91,
        "description": "Medefaidrin",
    },
    "Miao": {
        "start": 93952,
        "end": 94111,
        "code_points": 160,
        "assigned_characters": 149,
        "description": "Miao",
    },
    "Ideographic Symbols and Punctuation": {
        "start": 94176,
        "end": 94207,
        "code_points": 32,
        "assigned_characters": 7,
        "description": "Han (4 characters), Khitan Small Script (1 character), Nushu (1 character), Tangut (1 character)",
    },
    "Tangut": {
        "start": 94208,
        "end": 100351,
        "code_points": 6144,
        "assigned_characters": 6136,
        "description": "Tangut",
    },
    "Tangut Components": {
        "start": 100352,
        "end": 101119,
        "code_points": 768,
        "assigned_characters": 768,
        "description": "Tangut",
    },
    "Khitan Small Script": {
        "start": 101120,
        "end": 101631,
        "code_points": 512,
        "assigned_characters": 470,
        "description": "Khitan Small Script",
    },
    "Tangut Supplement": {
        "start": 101632,
        "end": 101759,
        "code_points": 128,
        "assigned_characters": 9,
        "description": "Tangut",
    },
    "Kana Extended-B": {
        "start": 110576,
        "end": 110591,
        "code_points": 16,
        "assigned_characters": 13,
        "description": "Katakana",
    },
    "Kana Supplement": {
        "start": 110592,
        "end": 110847,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Hiragana (255 characters), Katakana (1 character)",
    },
    "Kana Extended-A": {
        "start": 110848,
        "end": 110895,
        "code_points": 48,
        "assigned_characters": 35,
        "description": "Hiragana (32 characters), Katakana (3 characters)",
    },
    "Small Kana Extension": {
        "start": 110896,
        "end": 110959,
        "code_points": 64,
        "assigned_characters": 9,
        "description": "Hiragana (4 characters), Katakana (5 characters)",
    },
    "Nushu": {
        "start": 110960,
        "end": 111359,
        "code_points": 400,
        "assigned_characters": 396,
        "description": "Nüshu",
    },
    "Duployan": {
        "start": 113664,
        "end": 113823,
        "code_points": 160,
        "assigned_characters": 143,
        "description": "Duployan",
    },
    "Shorthand Format Controls": {
        "start": 113824,
        "end": 113839,
        "code_points": 16,
        "assigned_characters": 4,
        "description": "Common",
    },
    "Znamenny Musical Notation": {
        "start": 118528,
        "end": 118735,
        "code_points": 208,
        "assigned_characters": 185,
        "description": "Common (116 characters), Inherited (69 characters)",
    },
    "Byzantine Musical Symbols": {
        "start": 118784,
        "end": 119039,
        "code_points": 256,
        "assigned_characters": 246,
        "description": "Common",
    },
    "Musical Symbols": {
        "start": 119040,
        "end": 119295,
        "code_points": 256,
        "assigned_characters": 233,
        "description": "Common (211 characters), Inherited (22 characters)",
    },
    "Ancient Greek Musical Notation": {
        "start": 119296,
        "end": 119375,
        "code_points": 80,
        "assigned_characters": 70,
        "description": "Greek",
    },
    "Kaktovik Numerals": {
        "start": 119488,
        "end": 119519,
        "code_points": 32,
        "assigned_characters": 20,
        "description": "Common",
    },
    "Mayan Numerals": {
        "start": 119520,
        "end": 119551,
        "code_points": 32,
        "assigned_characters": 20,
        "description": "Common",
    },
    "Tai Xuan Jing Symbols": {
        "start": 119552,
        "end": 119647,
        "code_points": 96,
        "assigned_characters": 87,
        "description": "Common",
    },
    "Counting Rod Numerals": {
        "start": 119648,
        "end": 119679,
        "code_points": 32,
        "assigned_characters": 25,
        "description": "Common",
    },
    "Mathematical Alphanumeric Symbols": {
        "start": 119808,
        "end": 120831,
        "code_points": 1024,
        "assigned_characters": 996,
        "description": "Common",
    },
    "Sutton SignWriting": {
        "start": 120832,
        "end": 121519,
        "code_points": 688,
        "assigned_characters": 672,
        "description": "SignWriting",
    },
    "Latin Extended-G": {
        "start": 122624,
        "end": 122879,
        "code_points": 256,
        "assigned_characters": 37,
        "description": "Latin",
    },
    "Glagolitic Supplement": {
        "start": 122880,
        "end": 122927,
        "code_points": 48,
        "assigned_characters": 38,
        "description": "Glagolitic",
    },
    "Cyrillic Extended-D": {
        "start": 122928,
        "end": 123023,
        "code_points": 96,
        "assigned_characters": 63,
        "description": "Cyrillic",
    },
    "Nyiakeng Puachue Hmong": {
        "start": 123136,
        "end": 123215,
        "code_points": 80,
        "assigned_characters": 71,
        "description": "Nyiakeng Puachue Hmong",
    },
    "Toto": {
        "start": 123536,
        "end": 123583,
        "code_points": 48,
        "assigned_characters": 31,
        "description": "Toto",
    },
    "Wancho": {
        "start": 123584,
        "end": 123647,
        "code_points": 64,
        "assigned_characters": 59,
        "description": "Wancho",
    },
    "Nag Mundari": {
        "start": 124112,
        "end": 124159,
        "code_points": 48,
        "assigned_characters": 42,
        "description": "Mundari",
    },
    "Ethiopic Extended-B": {
        "start": 124896,
        "end": 124927,
        "code_points": 32,
        "assigned_characters": 28,
        "description": "Ethiopic",
    },
    "Mende Kikakui": {
        "start": 124928,
        "end": 125151,
        "code_points": 224,
        "assigned_characters": 213,
        "description": "Mende Kikakui",
    },
    "Adlam": {
        "start": 125184,
        "end": 125279,
        "code_points": 96,
        "assigned_characters": 88,
        "description": "Adlam",
    },
    "Indic Siyaq Numbers": {
        "start": 126064,
        "end": 126143,
        "code_points": 80,
        "assigned_characters": 68,
        "description": "Common",
    },
    "Ottoman Siyaq Numbers": {
        "start": 126208,
        "end": 126287,
        "code_points": 80,
        "assigned_characters": 61,
        "description": "Common",
    },
    "Arabic Mathematical Alphabetic Symbols": {
        "start": 126464,
        "end": 126719,
        "code_points": 256,
        "assigned_characters": 143,
        "description": "Arabic",
    },
    "Mahjong Tiles": {
        "start": 126976,
        "end": 127023,
        "code_points": 48,
        "assigned_characters": 44,
        "description": "Common",
    },
    "Domino Tiles": {
        "start": 127024,
        "end": 127135,
        "code_points": 112,
        "assigned_characters": 100,
        "description": "Common",
    },
    "Playing Cards": {
        "start": 127136,
        "end": 127231,
        "code_points": 96,
        "assigned_characters": 82,
        "description": "Common",
    },
    "Enclosed Alphanumeric Supplement": {
        "start": 127232,
        "end": 127487,
        "code_points": 256,
        "assigned_characters": 200,
        "description": "Common",
    },
    "Enclosed Ideographic Supplement": {
        "start": 127488,
        "end": 127743,
        "code_points": 256,
        "assigned_characters": 64,
        "description": "Hiragana (1 character), Common (63 characters)",
    },
    "Miscellaneous Symbols and Pictographs": {
        "start": 127744,
        "end": 128511,
        "code_points": 768,
        "assigned_characters": 768,
        "description": "Common",
    },
    "Emoticons": {
        "start": 128512,
        "end": 128591,
        "code_points": 80,
        "assigned_characters": 80,
        "description": "Common",
    },
    "Ornamental Dingbats": {
        "start": 128592,
        "end": 128639,
        "code_points": 48,
        "assigned_characters": 48,
        "description": "Common",
    },
    "Transport and Map Symbols": {
        "start": 128640,
        "end": 128767,
        "code_points": 128,
        "assigned_characters": 118,
        "description": "Common",
    },
    "Alchemical Symbols": {
        "start": 128768,
        "end": 128895,
        "code_points": 128,
        "assigned_characters": 124,
        "description": "Common",
    },
    "Geometric Shapes Extended": {
        "start": 128896,
        "end": 129023,
        "code_points": 128,
        "assigned_characters": 103,
        "description": "Common",
    },
    "Supplemental Arrows-C": {
        "start": 129024,
        "end": 129279,
        "code_points": 256,
        "assigned_characters": 150,
        "description": "Common",
    },
    "Supplemental Symbols and Pictographs": {
        "start": 129280,
        "end": 129535,
        "code_points": 256,
        "assigned_characters": 256,
        "description": "Common",
    },
    "Chess Symbols": {
        "start": 129536,
        "end": 129647,
        "code_points": 112,
        "assigned_characters": 98,
        "description": "Common",
    },
    "Symbols and Pictographs Extended-A": {
        "start": 129648,
        "end": 129791,
        "code_points": 144,
        "assigned_characters": 107,
        "description": "Common",
    },
    "Symbols for Legacy Computing": {
        "start": 129792,
        "end": 130047,
        "code_points": 256,
        "assigned_characters": 212,
        "description": "Common",
    },
    "CJK Unified Ideographs Extension B": {
        "start": 131072,
        "end": 173791,
        "code_points": 42720,
        "assigned_characters": 42720,
        "description": "Han",
    },
    "CJK Unified Ideographs Extension C": {
        "start": 173824,
        "end": 177983,
        "code_points": 4160,
        "assigned_characters": 4154,
        "description": "Han",
    },
    "CJK Unified Ideographs Extension D": {
        "start": 177984,
        "end": 178207,
        "code_points": 224,
        "assigned_characters": 222,
        "description": "Han",
    },
    "CJK Unified Ideographs Extension E": {
        "start": 178208,
        "end": 183983,
        "code_points": 5776,
        "assigned_characters": 5762,
        "description": "Han",
    },
    "CJK Unified Ideographs Extension F": {
        "start": 183984,
        "end": 191471,
        "code_points": 7488,
        "assigned_characters": 7473,
        "description": "Han",
    },
    "CJK Unified Ideographs Extension I": {
        "start": 191472,
        "end": 192095,
        "code_points": 624,
        "assigned_characters": 622,
        "description": "Han",
    },
    "CJK Compatibility Ideographs Supplement": {
        "start": 194560,
        "end": 195103,
        "code_points": 544,
        "assigned_characters": 542,
        "description": "Han",
    },
    "CJK Unified Ideographs Extension G": {
        "start": 196608,
        "end": 201551,
        "code_points": 4944,
        "assigned_characters": 4939,
        "description": "Han",
    },
    "CJK Unified Ideographs Extension H": {
        "start": 201552,
        "end": 205743,
        "code_points": 4192,
        "assigned_characters": 4192,
        "description": "Han",
    },
    "Tags": {
        "start": 917504,
        "end": 917631,
        "code_points": 128,
        "assigned_characters": 97,
        "description": "Common",
    },
    "Variation Selectors Supplement": {
        "start": 917760,
        "end": 917999,
        "code_points": 240,
        "assigned_characters": 240,
        "description": "Inherited",
    },
    "Supplementary Private Use Area-A": {
        "start": 983040,
        "end": 1048575,
        "code_points": 65536,
        "assigned_characters": 65534,
        "description": "Unknown",
    },
    "Supplementary Private Use Area-B": {
        "start": 1048576,
        "end": 1114111,
        "code_points": 65536,
        "assigned_characters": 65534,
        "description": "Unknown",
    },
}


def print_all_unicode_chars():
    wholestring = ""
    for key, item in unicode_dict.items():
        print(key)
        wholestring += key
        j = 1
        for i in range(item["start"], item["end"]):
            if j % 80 == 0:
                print("")
                wholestring += "\n"
            j += 1
            try:
                print(f"{(g := str(chr(i)))}", end="")
                wholestring += g

            except UnicodeEncodeError:
                print(f"\\u{i}", end="")

        print("\n")
        wholestring += "\n\n"
    return wholestring


def index_all(l, n):
    indototal = 0
    allindex = []
    while True:
        try:
            indno = l[indototal:].index(n)
            indototal += indno + 1
            allindex.append(indototal - 1)
        except ValueError:
            break
    return allindex


def parse_elements(symb1, symb2, text):
    textlist = list(text)
    kla1 = sorted(index_all(textlist, symb1), reverse=True)
    kla2 = sorted(index_all(textlist, symb2), reverse=False)
    goodresults = []
    aufresults = []
    zuresults = []
    goodresultsflat = []
    lilen = min([len(kla1), len(kla2)])
    oldlen = -1
    while len(aufresults) < lilen:
        allresultsfinal = []
        found = False
        for auf in sorted([uu for uu in kla1 if uu not in aufresults], reverse=True):
            if auf in goodresultsflat:
                continue
            for zu in sorted([uu for uu in kla2 if uu not in zuresults], reverse=False):
                if zu in goodresultsflat:
                    continue
                if auf >= zu:
                    continue
                t1 = text[auf : zu + 1]
                if t1.count(symb1) != t1.count(symb2):
                    continue
                allresultsfinal.append([zu - auf, auf, zu, t1])
                found = True
                break
            if found:
                break
        best = sorted(allresultsfinal, key=lambda x: x[0])[0]
        goodresults.append([*best])
        goodresultsflat.extend([best[1], best[2]])
        aufresults.append(best[1])
        zuresults.append(best[2])
        newlen = len(goodresults)
        if newlen <= oldlen:
            break
        oldlen = newlen

    allsorted = sorted(goodresults, key=lambda x: x[:3])
    for i in range(len(allsorted)):
        s = set(range(allsorted[i][1], allsorted[i][2] + 1))
        allsorted[i].extend([(tuple(sorted(list(s)))), s])

    allsorted2 = deepcopy(allsorted)
    for ini1, i in enumerate(allsorted2):
        asstring = []
        for ini2, j in enumerate(allsorted2):
            if ini1 == ini2:
                continue
            if i[-1] < j[-1]:
                asstring.append((j[-2]))
        allsorted[ini1].append(asstring)

    allsorted2 = deepcopy(allsorted)
    for ini1, i in enumerate(allsorted2):
        asstring = []
        for ini2, j in enumerate(allsorted2):
            if ini1 == ini2:
                continue
            if i[-2] > j[-2]:
                asstring.append((j[-3]))
        allsorted[ini1].append(asstring)

    return {
        k[4]: {
            "size": k[0],
            "start": k[1],
            "end": k[2],
            "text": k[3],
            "parents": sorted(k[6], key=len),
            "children": sorted(k[7], key=len, reverse=True),
        }
        for k in allsorted
    }


def parse_elements_multi_letters(symb1, symb2, text):
    startletter = ""
    endletter = ""
    for key, item in unicode_dict.items():
        for i in range(item["start"], item["end"]):
            try:
                g = str(chr(i))
                if g not in text:
                    if not startletter:
                        startletter = g
                        continue
                    if not endletter:
                        endletter = g
                        break
            except UnicodeEncodeError:
                continue
        if endletter:
            break
    text2 = text.replace(symb1, startletter)
    text2 = text2.replace(symb2, endletter)

    try:
        pe = parse_elements(startletter, endletter, text2)
    except Exception:
        return {}
    lookupdict = {}
    for key, item in pe.items():
        origtext = symb1 + item["text"][1:-1] + symb2
        origtextlen = len(origtext)

        indi = sorted(index_all(text, origtext))
        awv = key[0]
        indi = [x for x in indi if x >= awv][0]
        lookupdict[key] = tuple(range(indi, indi + origtextlen + 1))
    pe2 = {}
    for key, item in pe.items():
        newindex = lookupdict[key]
        pe2[newindex] = {
            "size": len(newindex),
            "start": newindex[0],
            "end": newindex[-1],
            "text": text[newindex[0] : newindex[-1]],
            "parents": [lookupdict[x] for x in item["parents"]],
            "children": [lookupdict[x] for x in item["children"]],
        }
    return pe2


def parse_elements_regex(re_open, re_close, text):
    if isinstance(re_open, str):
        re_open = re.compile(re_open)
    if isinstance(re_close, str):
        re_close = re.compile(re_close)
    results = {}
    for _symb1, _symb2 in itertools.product(
        (set(re_open.findall(text))), (set(re_close.findall(text)))
    ):
        try:
            results[(_symb1, _symb2)] = parse_elements_multi_letters(
                _symb1, _symb2, text
            )
        except Exception:
            continue
    return results


def parse_multipairs(open_close_pairs, text):
    results = {}
    for _symb1, _symb2 in open_close_pairs:
        try:
            results[(_symb1, _symb2)] = parse_elements_multi_letters(
                _symb1, _symb2, text
            )
        except Exception:
            continue
    return results


def parse_pairs(
    string: str,
    s1: Union[str, List[str], List[Tuple[str, str]], re.Pattern[str]],
    s2: Optional[Union[str, List[str], List[Tuple[str, str]], re.Pattern[str]]] = None,
    str_regex: bool = False,
) -> Dict[
    Union[str, Tuple[str, str]],
    Union[Dict[str, Any], Dict[Tuple[int, int], Dict[str, Any]]],
]:
    r"""
    Parses paired elements within a given string using specified delimiters.

    Args:
        string (str): The input text to be parsed.
        s1 (Union[str, List[Tuple[str, str]], re.Pattern[str]): The opening delimiter(s) to identify paired elements.
            - If a single string, it represents the opening delimiter for a single pair.
            - If a list of tuples, each tuple contains the opening and closing delimiters for multiple pairs.
            - If a regular expression pattern (compiled using re.compile), it defines the opening delimiter(s) using regex.
        s2 (Optional[Union[str, List[Tuple[str, str]], re.Pattern[str]]): The closing delimiter(s) for paired elements.
            - If a single string, it represents the closing delimiter for a single pair.
            - If a list of strings, each element from s1 must match the element with the corresponding index in s2
            - If None, each tuple in s1 contains the closing delimiter(s) for multiple pairs.
            - If a regular expression pattern (compiled using re.compile), it defines the closing delimiter(s) using regex.
        str_regex (bool): If True, treat s1 and s2 as regular expressions; if False, treat them as string delimiters.

    Returns:
        Dict[Union[str, Tuple[str, str]], Union[Dict[str, Any], Dict[Tuple[int, int], Dict[str, Any]]]: A dictionary where the keys are either a single pair (if s1 and s2 are strings) or a tuple of regular expression patterns (if s1 and s2 are regex patterns). The values are dictionaries describing the paired elements found in the input string.

    The dictionary structure for paired elements:
    - 'size': int - Size of the parsed element.
    - 'start': int - Starting index of the element in the input string.
    - 'end': int - Ending index of the element in the input string.
    - 'text': str - The text content of the parsed element.
    - 'parents': List[List[int]] - List of indices for elements that enclose the current element.
    - 'children': List[List[int]] - List of indices for elements enclosed by the current element.

    Examples:
        from parifinder import parse_pairs
        from pprint import pprint

        text_0 = '''[[1, 2, 2], [5], [2, 3]], 12: [[4, 4, 4], [12, 0], [6, 6]], 3: [[1, 2]][[1, 2, 2], [5], [2, 3]], 12: [[4, 4, 4], [12, 0], [6, 6]], 3: [[1, 2]]'''
        s1_0 = "["
        s2_0 = "]"
        r0 = parse_pairs(string=text_0, s1=s1_0, s2=s2_0, str_regex=False)
        print("r0-----------------------------------------------------------------")
        pprint(r0, indent=1, width=1)

        text_1 = "<body><p>a</p><p>a</p><p>The HTML <code>button</code> tag defines a clickable button.</p><p>x</p><p>The CSS <code>background-color</code> property defines the background color of an element.</p></body></html>"
        s1_1 = "<p>"
        s2_1 = "</p>"
        r1 = parse_pairs(string=text_1, s1=s1_1, s2=s2_1, str_regex=False)
        print("r1-----------------------------------------------------------------")
        pprint(r1, indent=1, width=1)

        text_2 = "[1bla[2bla/2]/1]"
        s1_2 = r"\[\d"
        s2_2 = r"/\d]"
        r2 = parse_pairs(string=text_2, s1=s1_2, s2=s2_2, str_regex=True)
        print("r2-----------------------------------------------------------------")
        pprint(r2, indent=1, width=1)

        text_3 = "[1bla[2bla/2]/1]"
        s1_3 = [("[1", "/1]"), ("[2", "/2]")]
        s2_3 = None
        r3 = parse_pairs(string=text_3, s1=s1_3, s2=s2_3, str_regex=False)
        print("r3-----------------------------------------------------------------")
        pprint(r3, indent=1, width=1)

        text_4 = "[1bla[2bla/2]/1]"
        s1_4 = ["[1", "[2"]
        s2_4 = ["/1]", "/2]"]
        r4 = parse_pairs(string=text_4, s1=s1_4, s2=s2_4, str_regex=False)
        print("r4-----------------------------------------------------------------")
        pprint(r4, indent=1, width=1)

    """
    if isinstance(s1, str) and isinstance(s2, str):
        if not str_regex:
            if len(s1) > 1 or len(s2) > 1:
                return parse_elements_multi_letters(s1, s2, string)
            else:
                return parse_elements(s1, s2, string)
        else:
            return parse_elements_regex(s1, s2, string)
    elif isinstance(s1, (list, tuple)) and (
        isinstance(s2, (list, tuple)) or isinstance(s2, type(None))
    ):
        if isinstance(s2, type(None)):
            return parse_multipairs(s1, string)
        else:
            return parse_multipairs([list(x) for x in zip(*[s1, s2])], string)
    else:
        return parse_elements_regex(s1, s2, string)
