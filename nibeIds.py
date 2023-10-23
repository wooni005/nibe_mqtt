idToDeviceName = {
    # 40083: "StroomFase1", #We hebben geen stroom opnemers
    # 40081: "StroomFase2",
    # 40079: "StroomFase3",
    40004: "Temp-Nibe-Buiten",
    40067: "Temp-Nibe-Buiten-gem",
    # 40033: "Temp Kamer", #We hebben geen thermostaat
    40008: "Temp-Verw.aanvoer",
    40012: "Temp-Verw.retour",
    40013: "Temp-WarmWater-boven",
    40014: "Temp-WarmWater-midden",
    40015: "Temp-Bron-in",
    40016: "Temp-Bron-uit",
    43005: "Graadminuten",
    43009: "Temp-Berekende-aanvoer",
    # 40022: "TempAanzuigGas",
    # 40017: "TempCondensorUit",
    # 40018: "TempHeetgas",
    # 40019: "TempVloeistofleiding",
    43437: "PompsnelheidCVsysteem",
    43439: "PompsnelheidBronpomp",
    10033: "BijverwarmingGeblokkeerd",
    # 47212: "BijverwarmingPmax",
    # 43084: "BijverwarmingPhuidig",
    44300: "TotaalWarmteInclBijv",
    44298: "TotaalWarmWaterInclBijv",
    43416: "Compressorstarts",
    # 43420: "BedrijfstijdComprTotaal",
    # 43424: "BedrijfstijdComprWarmw",
    10012: "CompressorGeblokkeerd",
}

deviceIntType = [
    "Graadminuten",
    "PompsnelheidCVsysteem",
    "PompsnelheidBronpomp",
    "Compressorstarts",
    "BedrijfstijdComprTotaal",
    "BedrijfstijdComprWarmw",
]

tempDevices = [
    "Temp-Nibe-Buiten",
    "Temp-Nibe-Buiten-gem",
    "Temp-Bron-in",
    "Temp-Bron-uit",
    "Temp-Berekende-aanvoer",
    "Temp-Verw.retour",
    "Temp-Verw.aanvoer",
    "Temp-WarmWater-boven",
    "Temp-WarmWater-midden",
]

valueConversion = {
    "True": 1,
    "true": 1,
    "ON":  1,
    "On":  1,
    "on":  1,
    "OK": 1,
    "Yes": 1,
    "yes": 1,
    "False": 0,
    "false": 0,
    "OFF": 0,
    "Off": 0,
    "off": 0,
    "LOW": 0,
    "No": 0,
    "no": 0,

    "ano": 1,
    "ne": 0,

    "nee": 0,
    "ja":  1,
    "uit": 0,
    "aan": 1
}
