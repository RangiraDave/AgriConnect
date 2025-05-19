import json
from django.core.management.base import BaseCommand
from core.models import Province, District, Sector, Cell, Village

class Command(BaseCommand):
    help = "Import hierarchical location data from JSON"

    def handle(self, *args, **kwargs):
        # Paste your JSON as a string (triple quotes)
        json_data = """
        { 
            "count": 5,
            "next": null,
            "previous": null,
            "results": [
                {
                  "id": 2,
                  "name": "Eastern Province",
                  "code": "ep",
                  "districts": [
                    {
                      "id": 12,
                      "name": "Bugesera",
                      "code": "bu",
                      "sectors": [
                        {
                          "id": 52,
                          "name": "Gashora",
                          "code": "gas",
                          "cells": [
                            {
                              "id": 3,
                              "name": "Biryogo",
                              "code": "biry",
                              "villages": []
                            },
                            {
                              "id": 4,
                              "name": "Kabuye",
                              "code": "kabu",
                              "villages": []
                            },
                            {
                              "id": 5,
                              "name": "Mwendo",
                              "code": "mwe",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 53,
                          "name": "Mayange",
                          "code": "maya",
                          "cells": [
                            {
                              "id": 6,
                              "name": "Kagamba",
                              "code": "kagam",
                              "villages": []
                            },
                            {
                              "id": 7,
                              "name": "Kibenga",
                              "code": "kibe",
                              "villages": []
                            },
                            {
                              "id": 8,
                              "name": "Kibirizi",
                              "code": "kibi",
                              "villages": []
                            },
                            {
                              "id": 9,
                              "name": "Mbyo",
                              "code": "mby",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 54,
                          "name": "Nyamata",
                          "code": "nyama",
                          "cells": [
                            {
                              "id": 10,
                              "name": "Kanazi",
                              "code": "kana",
                              "villages": []
                            },
                            {
                              "id": 11,
                              "name": "Kayumba",
                              "code": "kayu",
                              "villages": []
                            },
                            {
                              "id": 12,
                              "name": "Maranyundo",
                              "code": "mara",
                              "villages": []
                            },
                            {
                              "id": 13,
                              "name": "Murama",
                              "code": "mura",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 55,
                          "name": "Rilima",
                          "code": "rili",
                          "cells": [
                            {
                              "id": 14,
                              "name": "Kabeza",
                              "code": "kabe",
                              "villages": []
                            },
                            {
                              "id": 15,
                              "name": "Karera",
                              "code": "kare",
                              "villages": []
                            },
                            {
                              "id": 16,
                              "name": "Ntarama",
                              "code": "ntara",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 56,
                          "name": "Rweru",
                          "code": "rwer",
                          "cells": [
                            {
                              "id": 17,
                              "name": "Batima",
                              "code": "bati",
                              "villages": []
                            },
                            {
                              "id": 18,
                              "name": "Kintambwe",
                              "code": "kinta",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 57,
                          "name": "Shyara",
                          "code": "shya",
                          "cells": [
                            {
                              "id": 37,
                              "name": "Kagitega",
                              "code": "kagite",
                              "villages": []
                            }
                          ]
                        }
                      ]
                    },
                    {
                      "id": 4,
                      "name": "Gatsibo",
                      "code": "gd",
                      "sectors": [
                        {
                          "id": 3,
                          "name": "Gasange",
                          "code": "gasa",
                          "cells": []
                        },
                        {
                          "id": 4,
                          "name": "Gitoki",
                          "code": "gito",
                          "cells": []
                        },
                        {
                          "id": 5,
                          "name": "Kabarore",
                          "code": "kaba",
                          "cells": []
                        },
                        {
                          "id": 6,
                          "name": "Kageyo",
                          "code": "kage",
                          "cells": []
                        },
                        {
                          "id": 7,
                          "name": "Kiziguro",
                          "code": "kizi",
                          "cells": []
                        },
                        {
                          "id": 8,
                          "name": "Muhura",
                          "code": "muhu",
                          "cells": []
                        },
                        {
                          "id": 9,
                          "name": "Murambi",
                          "code": "mura",
                          "cells": []
                        },
                        {
                          "id": 10,
                          "name": "Ngarama",
                          "code": "ngara",
                          "cells": []
                        },
                        {
                          "id": 11,
                          "name": "Nyagihanga",
                          "code": "nyagi",
                          "cells": []
                        },
                        {
                          "id": 12,
                          "name": "Remera",
                          "code": "rem",
                          "cells": []
                        },
                        {
                          "id": 2,
                          "name": "Rugarama",
                          "code": "Rug",
                          "cells": [
                            {
                              "id": 2,
                              "name": "Kanyangese",
                              "code": "Kany",
                              "villages": [
                                {
                                  "id": 2,
                                  "name": "Kabeza",
                                  "code": "Kab"
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "id": 14,
                          "name": "Rwimbogo",
                          "code": "rwi",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 3,
                      "name": "Kayonza",
                      "code": "kd",
                      "sectors": [
                        {
                          "id": 23,
                          "name": "Gahini",
                          "code": "gahi",
                          "cells": []
                        },
                        {
                          "id": 24,
                          "name": "Kabare",
                          "code": "kab",
                          "cells": []
                        },
                        {
                          "id": 25,
                          "name": "Mukarange",
                          "code": "muk",
                          "cells": []
                        },
                        {
                          "id": 26,
                          "name": "Murama",
                          "code": "mur",
                          "cells": []
                        },
                        {
                          "id": 27,
                          "name": "Ndego",
                          "code": "nde",
                          "cells": []
                        },
                        {
                          "id": 28,
                          "name": "Nyamirama",
                          "code": "nya",
                          "cells": []
                        },
                        {
                          "id": 30,
                          "name": "Nyamirama",
                          "code": "nyam",
                          "cells": []
                        },
                        {
                          "id": 29,
                          "name": "Rukara",
                          "code": "ruka",
                          "cells": []
                        },
                        {
                          "id": 31,
                          "name": "Rwinkwavu",
                          "code": "rwink",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 6,
                      "name": "Kirehe",
                      "code": "kid",
                      "sectors": [
                        {
                          "id": 32,
                          "name": "Gahara",
                          "code": "gah",
                          "cells": []
                        },
                        {
                          "id": 33,
                          "name": "Mahama",
                          "code": "maha",
                          "cells": []
                        },
                        {
                          "id": 34,
                          "name": "Mpanga",
                          "code": "mpa",
                          "cells": []
                        },
                        {
                          "id": 35,
                          "name": "Nasho",
                          "code": "nas",
                          "cells": []
                        },
                        {
                          "id": 37,
                          "name": "Nyamugari",
                          "code": "nyamu",
                          "cells": []
                        },
                        {
                          "id": 36,
                          "name": "Nyarubuye",
                          "code": "nyar",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 7,
                      "name": "Ngoma",
                      "code": "ngo",
                      "sectors": [
                        {
                          "id": 38,
                          "name": "Gashanda",
                          "code": "gash",
                          "cells": []
                        },
                        {
                          "id": 39,
                          "name": "Karembo",
                          "code": "kare",
                          "cells": []
                        },
                        {
                          "id": 40,
                          "name": "Kazo",
                          "code": "kaz",
                          "cells": []
                        },
                        {
                          "id": 41,
                          "name": "Mugesera",
                          "code": "muge",
                          "cells": []
                        },
                        {
                          "id": 42,
                          "name": "Rukumberi",
                          "code": "ruku",
                          "cells": []
                        },
                        {
                          "id": 43,
                          "name": "Sake",
                          "code": "sak",
                          "cells": []
                        },
                        {
                          "id": 44,
                          "name": "Zaza",
                          "code": "zaz",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 5,
                      "name": "Nyagatare",
                      "code": "nd",
                      "sectors": [
                        {
                          "id": 15,
                          "name": "Gatunda",
                          "code": "gatu",
                          "cells": []
                        },
                        {
                          "id": 16,
                          "name": "Karama",
                          "code": "kar",
                          "cells": []
                        },
                        {
                          "id": 17,
                          "name": "Karangazi",
                          "code": "kara",
                          "cells": []
                        },
                        {
                          "id": 18,
                          "name": "Matimba",
                          "code": "mati",
                          "cells": []
                        },
                        {
                          "id": 19,
                          "name": "Mukama",
                          "code": "muka",
                          "cells": []
                        },
                        {
                          "id": 20,
                          "name": "Rwempasha",
                          "code": "rwe",
                          "cells": []
                        },
                        {
                          "id": 21,
                          "name": "Rwimiyaga",
                          "code": "rwim",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 8,
                      "name": "Rwamagana",
                      "code": "rwa",
                      "sectors": [
                        {
                          "id": 45,
                          "name": "Gishali",
                          "code": "gish",
                          "cells": [
                            {
                              "id": 50,
                              "name": "Kabasore",
                              "code": "kaba",
                              "villages": []
                            },
                            {
                              "id": 51,
                              "name": "Karenge",
                              "code": "kareng",
                              "villages": []
                            },
                            {
                              "id": 49,
                              "name": "Ruhimbi",
                              "code": "Ruhi",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 46,
                          "name": "Kigabiro",
                          "code": "kiga",
                          "cells": []
                        },
                        {
                          "id": 47,
                          "name": "Muhazi",
                          "code": "muha",
                          "cells": [
                            {
                              "id": 52,
                              "name": "Karitutu",
                              "code": "karit",
                              "villages": []
                            },
                            {
                              "id": 53,
                              "name": "Nsinda",
                              "code": "nsin",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 48,
                          "name": "Musha",
                          "code": "mus",
                          "cells": [
                            {
                              "id": 54,
                              "name": "Akabare",
                              "code": "akab",
                              "villages": []
                            },
                            {
                              "id": 56,
                              "name": "Musha",
                              "code": "mush",
                              "villages": []
                            },
                            {
                              "id": 55,
                              "name": "Nyakabanda",
                              "code": "nyakab",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 49,
                          "name": "Muyumbu",
                          "code": "muyu",
                          "cells": [
                            {
                              "id": 58,
                              "name": "Gatare",
                              "code": "gata",
                              "villages": []
                            },
                            {
                              "id": 57,
                              "name": "Munini",
                              "code": "muni",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 50,
                          "name": "Nzige",
                          "code": "nzi",
                          "cells": []
                        },
                        {
                          "id": 51,
                          "name": "Rubona",
                          "code": "rubo",
                          "cells": []
                        },
                        {
                          "id": 22,
                          "name": "Tabagwe",
                          "code": "taba",
                          "cells": []
                        }
                      ]
                    }
                  ]
                },
                {
                  "id": 1,
                  "name": "Kigali City",
                  "code": "kc",
                  "districts": [
                    {
                      "id": 11,
                      "name": "Gasabo",
                      "code": "ga",
                      "sectors": [
                        {
                          "id": 58,
                          "name": "Bumbogo",
                          "code": "bumb",
                          "cells": []
                        },
                        {
                          "id": 59,
                          "name": "Gatsata",
                          "code": "gatsa",
                          "cells": []
                        },
                        {
                          "id": 61,
                          "name": "Gisozi",
                          "code": "giso",
                          "cells": []
                        },
                        {
                          "id": 62,
                          "name": "Jabana",
                          "code": "jaba",
                          "cells": []
                        },
                        {
                          "id": 60,
                          "name": "Jali",
                          "code": "ja",
                          "cells": []
                        },
                        {
                          "id": 65,
                          "name": "Kacyiru",
                          "code": "kacy",
                          "cells": []
                        },
                        {
                          "id": 66,
                          "name": "Kimironko",
                          "code": "kim",
                          "cells": []
                        },
                        {
                          "id": 63,
                          "name": "Kinyinya",
                          "code": "kiny",
                          "cells": []
                        },
                        {
                          "id": 64,
                          "name": "Ndera",
                          "code": "nder",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 10,
                      "name": "Kicukiro",
                      "code": "ki",
                      "sectors": [
                        {
                          "id": 67,
                          "name": "Gahanga",
                          "code": "gaha",
                          "cells": []
                        },
                        {
                          "id": 68,
                          "name": "Gatenga",
                          "code": "gate",
                          "cells": []
                        },
                        {
                          "id": 69,
                          "name": "Gikondo",
                          "code": "giko",
                          "cells": []
                        },
                        {
                          "id": 71,
                          "name": "Kagarama",
                          "code": "kagara",
                          "cells": []
                        },
                        {
                          "id": 70,
                          "name": "Kanombe",
                          "code": "kano",
                          "cells": []
                        },
                        {
                          "id": 73,
                          "name": "Masaka",
                          "code": "masa",
                          "cells": []
                        },
                        {
                          "id": 72,
                          "name": "Niboye",
                          "code": "nibo",
                          "cells": []
                        },
                        {
                          "id": 74,
                          "name": "Nyarugunga",
                          "code": "nyaru",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 9,
                      "name": "Nyarugenge",
                      "code": "nya",
                      "sectors": [
                        {
                          "id": 75,
                          "name": "Gitega",
                          "code": "git",
                          "cells": []
                        },
                        {
                          "id": 76,
                          "name": "Kanyinya",
                          "code": "kany",
                          "cells": []
                        },
                        {
                          "id": 77,
                          "name": "Kimisagara",
                          "code": "kimi",
                          "cells": []
                        },
                        {
                          "id": 78,
                          "name": "Muhima",
                          "code": "muhi",
                          "cells": []
                        },
                        {
                          "id": 79,
                          "name": "Nyamirambo",
                          "code": "nyami",
                          "cells": []
                        },
                        {
                          "id": 80,
                          "name": "Rwezamenyo",
                          "code": "rweza",
                          "cells": []
                        }
                      ]
                    }
                  ]
                },
                {
                  "id": 3,
                  "name": "Northern province",
                  "code": "np",
                  "districts": [
                    {
                      "id": 16,
                      "name": "Burera",
                      "code": "bur",
                      "sectors": [
                        {
                          "id": 112,
                          "name": "Bungwe",
                          "code": "bung",
                          "cells": [
                            {
                              "id": 19,
                              "name": "Bushenya",
                              "code": "bushe",
                              "villages": []
                            },
                            {
                              "id": 33,
                              "name": "Kidakama",
                              "code": "kidaka",
                              "villages": []
                            },
                            {
                              "id": 20,
                              "name": "Mudugari",
                              "code": "mudu",
                              "villages": []
                            },
                            {
                              "id": 21,
                              "name": "Tumba",
                              "code": "tumb",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 113,
                          "name": "Butaro",
                          "code": "buta",
                          "cells": [
                            {
                              "id": 59,
                              "name": "Bungwe",
                              "code": "bungw",
                              "villages": []
                            },
                            {
                              "id": 60,
                              "name": "Bushenya",
                              "code": "bushen",
                              "villages": []
                            },
                            {
                              "id": 24,
                              "name": "Gisovu",
                              "code": "giso",
                              "villages": []
                            },
                            {
                              "id": 22,
                              "name": "Mubuga",
                              "code": "mubu",
                              "villages": []
                            },
                            {
                              "id": 61,
                              "name": "Mudugali",
                              "code": "muduga",
                              "villages": []
                            },
                            {
                              "id": 41,
                              "name": "Nyamicucu",
                              "code": "nyami",
                              "villages": []
                            },
                            {
                              "id": 42,
                              "name": "Rusumo",
                              "code": "Rusu",
                              "villages": []
                            },
                            {
                              "id": 23,
                              "name": "Rusumo",
                              "code": "rusu",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 114,
                          "name": "Cyanika",
                          "code": "cyani",
                          "cells": [
                            {
                              "id": 31,
                              "name": "Gabiro",
                              "code": "gabi",
                              "villages": []
                            },
                            {
                              "id": 43,
                              "name": "Gasiza",
                              "code": "gasi",
                              "villages": []
                            },
                            {
                              "id": 44,
                              "name": "Gasiza",
                              "code": "gasiz",
                              "villages": []
                            },
                            {
                              "id": 66,
                              "name": "GISOVU",
                              "code": "Giso",
                              "villages": []
                            },
                            {
                              "id": 25,
                              "name": "Kabyiniro",
                              "code": "kabyi",
                              "villages": []
                            },
                            {
                              "id": 45,
                              "name": "Kabyiniro",
                              "code": "kabyin",
                              "villages": []
                            },
                            {
                              "id": 67,
                              "name": "KABYINIRO",
                              "code": "kabyini",
                              "villages": []
                            },
                            {
                              "id": 32,
                              "name": "Kagerero",
                              "code": "kage",
                              "villages": []
                            },
                            {
                              "id": 46,
                              "name": "Kagitega",
                              "code": "kagit",
                              "villages": []
                            },
                            {
                              "id": 47,
                              "name": "Kamanyana",
                              "code": "kamany",
                              "villages": []
                            },
                            {
                              "id": 63,
                              "name": "Mubuga",
                              "code": "mubag",
                              "villages": []
                            },
                            {
                              "id": 64,
                              "name": "Muhotora",
                              "code": "muhoto",
                              "villages": []
                            },
                            {
                              "id": 48,
                              "name": "Nyagahinga",
                              "code": "nyagahi",
                              "villages": []
                            },
                            {
                              "id": 65,
                              "name": "Nyamicucu",
                              "code": "nyamicu",
                              "villages": []
                            },
                            {
                              "id": 62,
                              "name": "Tumba",
                              "code": "tumba",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 115,
                          "name": "Cyeru",
                          "code": "cye",
                          "cells": [
                            {
                              "id": 38,
                              "name": "Buramba",
                              "code": "buram",
                              "villages": []
                            },
                            {
                              "id": 71,
                              "name": "BURAMBA",
                              "code": "buramb",
                              "villages": []
                            },
                            {
                              "id": 68,
                              "name": "BUTARE",
                              "code": "butar",
                              "villages": []
                            },
                            {
                              "id": 40,
                              "name": "Gabiro",
                              "code": "gab",
                              "villages": []
                            },
                            {
                              "id": 26,
                              "name": "Kagitega",
                              "code": "kagi",
                              "villages": []
                            },
                            {
                              "id": 69,
                              "name": "NDONGOZI",
                              "code": "ndongo",
                              "villages": []
                            },
                            {
                              "id": 70,
                              "name": "RUYANGE",
                              "code": "ruya",
                              "villages": []
                            },
                            {
                              "id": 39,
                              "name": "Rwasa",
                              "code": "rwa",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 116,
                          "name": "Gahunga",
                          "code": "gahu",
                          "cells": [
                            {
                              "id": 27,
                              "name": "Kamanyana",
                              "code": "kaman",
                              "villages": []
                            },
                            {
                              "id": 72,
                              "name": "MUSENDA",
                              "code": "muse",
                              "villages": []
                            },
                            {
                              "id": 74,
                              "name": "MUSENDA",
                              "code": "musend",
                              "villages": []
                            },
                            {
                              "id": 73,
                              "name": "RWAMBOGO",
                              "code": "rwambo",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 119,
                          "name": "Gatebe",
                          "code": "gateb",
                          "cells": [
                            {
                              "id": 36,
                              "name": "Gisovu",
                              "code": "gisov",
                              "villages": []
                            },
                            {
                              "id": 75,
                              "name": "MUSASA",
                              "code": "musas",
                              "villages": []
                            },
                            {
                              "id": 28,
                              "name": "Nyagahinga",
                              "code": "nyaga",
                              "villages": []
                            },
                            {
                              "id": 76,
                              "name": "RUNOGA",
                              "code": "runog",
                              "villages": []
                            },
                            {
                              "id": 34,
                              "name": "Rwasa",
                              "code": "rwas",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 117,
                          "name": "Gitovu",
                          "code": "gitov",
                          "cells": [
                            {
                              "id": 29,
                              "name": "Buramba",
                              "code": "bura",
                              "villages": []
                            },
                            {
                              "id": 77,
                              "name": "KABAYA",
                              "code": "kabay",
                              "villages": []
                            },
                            {
                              "id": 78,
                              "name": "KAYENZI",
                              "code": "kayenz",
                              "villages": []
                            },
                            {
                              "id": 79,
                              "name": "KIRINGA",
                              "code": "kirin",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 118,
                          "name": "Kivuye",
                          "code": "kivuy",
                          "cells": [
                            {
                              "id": 82,
                              "name": "BUGAMBA",
                              "code": "bugam",
                              "villages": []
                            },
                            {
                              "id": 84,
                              "name": "BUKWASHURI",
                              "code": "bukwash",
                              "villages": []
                            },
                            {
                              "id": 35,
                              "name": "Gabiro",
                              "code": "gabir",
                              "villages": []
                            },
                            {
                              "id": 83,
                              "name": "KAGANDA",
                              "code": "kagand",
                              "villages": []
                            },
                            {
                              "id": 30,
                              "name": "Kidakama",
                              "code": "kida",
                              "villages": []
                            },
                            {
                              "id": 80,
                              "name": "NKUMBA",
                              "code": "nkumb",
                              "villages": []
                            },
                            {
                              "id": 81,
                              "name": "NTARUKA",
                              "code": "ntaruk",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 121,
                          "name": "Rusarabuye",
                          "code": "rusa",
                          "cells": [
                            {
                              "id": 87,
                              "name": "KIVUMU",
                              "code": "kivum",
                              "villages": []
                            },
                            {
                              "id": 88,
                              "name": "NYAMUGALI",
                              "code": "nyamug",
                              "villages": []
                            },
                            {
                              "id": 85,
                              "name": "NYIRATABA",
                              "code": "nyirata",
                              "villages": []
                            },
                            {
                              "id": 86,
                              "name": "NYIRATABA",
                              "code": "nyirat",
                              "villages": []
                            },
                            {
                              "id": 90,
                              "name": "RUKANDABYUMA",
                              "code": "rukandab",
                              "villages": []
                            },
                            {
                              "id": 89,
                              "name": "RUSHARA",
                              "code": "rusha",
                              "villages": []
                            }
                          ]
                        }
                      ]
                    },
                    {
                      "id": 17,
                      "name": "Gakenke",
                      "code": "gak",
                      "sectors": [
                        {
                          "id": 101,
                          "name": "Busengo",
                          "code": "bus",
                          "cells": [
                            {
                              "id": 91,
                              "name": "BUTERERI",
                              "code": "butere",
                              "villages": []
                            },
                            {
                              "id": 92,
                              "name": "BYIBUHIRO",
                              "code": "byibu",
                              "villages": []
                            },
                            {
                              "id": 93,
                              "name": "KAMINA",
                              "code": "kami",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 102,
                          "name": "Coko",
                          "code": "cok",
                          "cells": [
                            {
                              "id": 94,
                              "name": "KIRUKU",
                              "code": "kiruk",
                              "villages": []
                            },
                            {
                              "id": 95,
                              "name": "MBIRIMA",
                              "code": "mbiri",
                              "villages": []
                            },
                            {
                              "id": 97,
                              "name": "MUHORORO",
                              "code": "muhoro",
                              "villages": []
                            },
                            {
                              "id": 96,
                              "name": "NYANGE",
                              "code": "nyang",
                              "villages": []
                            },
                            {
                              "id": 98,
                              "name": "RUKORE",
                              "code": "ruko",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 103,
                          "name": "Cyabingo",
                          "code": "cyab",
                          "cells": [
                            {
                              "id": 99,
                              "name": "BUHETA",
                              "code": "buhe",
                              "villages": []
                            },
                            {
                              "id": 100,
                              "name": "KAGOMA",
                              "code": "kago",
                              "villages": []
                            },
                            {
                              "id": 101,
                              "name": "NGANZO",
                              "code": "nganz",
                              "villages": []
                            },
                            {
                              "id": 103,
                              "name": "NYACYINA",
                              "code": "nyacyi",
                              "villages": []
                            },
                            {
                              "id": 102,
                              "name": "RUSAGARA",
                              "code": "rusaga",
                              "villages": []
                            },
                            {
                              "id": 104,
                              "name": "RUTENDERI",
                              "code": "rutende",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 104,
                          "name": "Janja",
                          "code": "jan",
                          "cells": [
                            {
                              "id": 105,
                              "name": "GASHYAMBA",
                              "code": "gashyam",
                              "villages": []
                            },
                            {
                              "id": 106,
                              "name": "GATWA",
                              "code": "gatw",
                              "villages": []
                            },
                            {
                              "id": 108,
                              "name": "KAMUBUGA",
                              "code": "kamubu",
                              "villages": []
                            },
                            {
                              "id": 110,
                              "name": "KANYANZA",
                              "code": "kanyan",
                              "villages": []
                            },
                            {
                              "id": 107,
                              "name": "KARUKUNGU",
                              "code": "karuku",
                              "villages": []
                            },
                            {
                              "id": 109,
                              "name": "MBATABATA",
                              "code": "mbataba",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 105,
                          "name": "kamubuga",
                          "code": "kamu",
                          "cells": [
                            {
                              "id": 115,
                              "name": "BUYANGE",
                              "code": "buyan",
                              "villages": []
                            },
                            {
                              "id": 111,
                              "name": "CYINTARE",
                              "code": "cyinta",
                              "villages": []
                            },
                            {
                              "id": 112,
                              "name": "RUGIMBU",
                              "code": "rugim",
                              "villages": []
                            },
                            {
                              "id": 113,
                              "name": "RUHINGA",
                              "code": "ruhin",
                              "villages": []
                            },
                            {
                              "id": 114,
                              "name": "SERERI",
                              "code": "sere",
                              "villages": []
                            },
                            {
                              "id": 116,
                              "name": "TANDAGURA",
                              "code": "tandagu",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 106,
                          "name": "Mataba",
                          "code": "mata",
                          "cells": [
                            {
                              "id": 127,
                              "name": "BURANGA",
                              "code": "burang",
                              "villages": []
                            },
                            {
                              "id": 119,
                              "name": "GAHINGA",
                              "code": "gahin",
                              "villages": []
                            },
                            {
                              "id": 125,
                              "name": "KIRYAMO",
                              "code": "kirya",
                              "villages": []
                            },
                            {
                              "id": 117,
                              "name": "MUNYANA",
                              "code": "munya",
                              "villages": []
                            },
                            {
                              "id": 118,
                              "name": "MURAMBI",
                              "code": "muram",
                              "villages": []
                            },
                            {
                              "id": 122,
                              "name": "MUSAGARA",
                              "code": "musaga",
                              "villages": []
                            },
                            {
                              "id": 123,
                              "name": "MUSENYI",
                              "code": "museny",
                              "villages": []
                            },
                            {
                              "id": 126,
                              "name": "MWIYANDO",
                              "code": "mwiya",
                              "villages": []
                            },
                            {
                              "id": 121,
                              "name": "NKOMANE",
                              "code": "nkoman",
                              "villages": []
                            },
                            {
                              "id": 120,
                              "name": "NKOMANE",
                              "code": "nkoma",
                              "villages": []
                            },
                            {
                              "id": 124,
                              "name": "RUGANDA",
                              "code": "rugan",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 111,
                          "name": "Minazi",
                          "code": "mina",
                          "cells": [
                            {
                              "id": 131,
                              "name": "BULIMBA",
                              "code": "bulim",
                              "villages": []
                            },
                            {
                              "id": 132,
                              "name": "BUSANANE",
                              "code": "busana",
                              "villages": []
                            },
                            {
                              "id": 129,
                              "name": "BUSORO",
                              "code": "buso",
                              "villages": []
                            },
                            {
                              "id": 128,
                              "name": "GAHINGA",
                              "code": "gahing",
                              "villages": []
                            },
                            {
                              "id": 133,
                              "name": "KAGEYO",
                              "code": "kagey",
                              "villages": []
                            },
                            {
                              "id": 134,
                              "name": "RWANKUBA",
                              "code": "rwank",
                              "villages": []
                            },
                            {
                              "id": 130,
                              "name": "RWESERO",
                              "code": "rwese",
                              "villages": []
                            },
                            {
                              "id": 135,
                              "name": "SHYOMBWE",
                              "code": "shyomb",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 107,
                          "name": "Muhondo",
                          "code": "muho",
                          "cells": []
                        },
                        {
                          "id": 108,
                          "name": "Muzo",
                          "code": "mu",
                          "cells": []
                        },
                        {
                          "id": 109,
                          "name": "Nemba",
                          "code": "nem",
                          "cells": []
                        },
                        {
                          "id": 120,
                          "name": "Rugendabari",
                          "code": "rugend",
                          "cells": []
                        },
                        {
                          "id": 110,
                          "name": "Ruli",
                          "code": "rul",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 18,
                      "name": "Gicumbi",
                      "code": "gi",
                      "sectors": [
                        {
                          "id": 93,
                          "name": "Byumba",
                          "code": "byu",
                          "cells": [
                            {
                              "id": 136,
                              "name": "KIGABIRO",
                              "code": "kigabi",
                              "villages": []
                            }
                          ]
                        },
                        {
                          "id": 94,
                          "name": "Cyumba",
                          "code": "cyum",
                          "cells": []
                        },
                        {
                          "id": 95,
                          "name": "Kaniga",
                          "code": "kanig",
                          "cells": []
                        },
                        {
                          "id": 96,
                          "name": "manyagiro",
                          "code": "manya",
                          "cells": []
                        },
                        {
                          "id": 97,
                          "name": "Miyove",
                          "code": "miyo",
                          "cells": []
                        },
                        {
                          "id": 100,
                          "name": "Mutete",
                          "code": "mute",
                          "cells": []
                        },
                        {
                          "id": 98,
                          "name": "Rukomo",
                          "code": "ruko",
                          "cells": []
                        },
                        {
                          "id": 99,
                          "name": "Rutare",
                          "code": "ruta",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 19,
                      "name": "Musanze",
                      "code": "mus",
                      "sectors": [
                        {
                          "id": 122,
                          "name": "Busogo",
                          "code": "buso",
                          "cells": []
                        },
                        {
                          "id": 123,
                          "name": "Cyuve",
                          "code": "cyuv",
                          "cells": []
                        },
                        {
                          "id": 124,
                          "name": "Gacaca",
                          "code": "gaca",
                          "cells": []
                        },
                        {
                          "id": 125,
                          "name": "Gashaki",
                          "code": "gasha",
                          "cells": []
                        },
                        {
                          "id": 126,
                          "name": "Kimonyi",
                          "code": "kimo",
                          "cells": []
                        },
                        {
                          "id": 127,
                          "name": "Kinigi",
                          "code": "kinig",
                          "cells": []
                        },
                        {
                          "id": 128,
                          "name": "Muhoza",
                          "code": "muhoz",
                          "cells": []
                        },
                        {
                          "id": 129,
                          "name": "Nyange",
                          "code": "nyang",
                          "cells": []
                        },
                        {
                          "id": 130,
                          "name": "Remera",
                          "code": "reme",
                          "cells": []
                        },
                        {
                          "id": 131,
                          "name": "Rwaza",
                          "code": "rwaz",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 20,
                      "name": "Rulindo",
                      "code": "rul",
                      "sectors": [
                        {
                          "id": 81,
                          "name": "Base",
                          "code": "bas",
                          "cells": []
                        },
                        {
                          "id": 92,
                          "name": "Bukure",
                          "code": "buk",
                          "cells": []
                        },
                        {
                          "id": 82,
                          "name": "Burega",
                          "code": "bur",
                          "cells": []
                        },
                        {
                          "id": 83,
                          "name": "Bushoki",
                          "code": "bush",
                          "cells": []
                        },
                        {
                          "id": 84,
                          "name": "Cyungo",
                          "code": "cyu",
                          "cells": []
                        },
                        {
                          "id": 85,
                          "name": "Kinihira",
                          "code": "kini",
                          "cells": []
                        },
                        {
                          "id": 86,
                          "name": "Kisaro",
                          "code": "kisa",
                          "cells": []
                        },
                        {
                          "id": 87,
                          "name": "Masoro",
                          "code": "maso",
                          "cells": []
                        },
                        {
                          "id": 88,
                          "name": "Mbogo",
                          "code": "mbo",
                          "cells": []
                        },
                        {
                          "id": 89,
                          "name": "Murambi",
                          "code": "muramb",
                          "cells": []
                        },
                        {
                          "id": 90,
                          "name": "Shyorongi",
                          "code": "shyo",
                          "cells": []
                        },
                        {
                          "id": 91,
                          "name": "Tumba",
                          "code": "tu",
                          "cells": []
                        }
                      ]
                    }
                  ]
                },
                {
                  "id": 5,
                  "name": "Southern Province",
                  "code": "sp",
                  "districts": [
                    {
                      "id": 13,
                      "name": "Gisagara",
                      "code": "gis",
                      "sectors": [
                        {
                          "id": 173,
                          "name": "Gikonko",
                          "code": "gikonk",
                          "cells": []
                        },
                        {
                          "id": 174,
                          "name": "Gishubi",
                          "code": "gishub",
                          "cells": []
                        },
                        {
                          "id": 175,
                          "name": "Kansi",
                          "code": "kans",
                          "cells": []
                        },
                        {
                          "id": 176,
                          "name": "Kibilizi",
                          "code": "kibil",
                          "cells": []
                        },
                        {
                          "id": 177,
                          "name": "Kigembe",
                          "code": "kigem",
                          "cells": []
                        },
                        {
                          "id": 178,
                          "name": "Mamba",
                          "code": "mamb",
                          "cells": []
                        },
                        {
                          "id": 179,
                          "name": "Muganza",
                          "code": "mugan",
                          "cells": []
                        },
                        {
                          "id": 180,
                          "name": "Mugombwa",
                          "code": "mugom",
                          "cells": []
                        },
                        {
                          "id": 181,
                          "name": "Mukindo",
                          "code": "muki",
                          "cells": []
                        },
                        {
                          "id": 182,
                          "name": "Musha",
                          "code": "mush",
                          "cells": []
                        },
                        {
                          "id": 183,
                          "name": "Nyanza",
                          "code": "nyan",
                          "cells": []
                        },
                        {
                          "id": 184,
                          "name": "Save",
                          "code": "sav",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 21,
                      "name": "Huye",
                      "code": "hu",
                      "sectors": [
                        {
                          "id": 166,
                          "name": "Gishavu",
                          "code": "gisha",
                          "cells": []
                        },
                        {
                          "id": 167,
                          "name": "Mukura",
                          "code": "muku",
                          "cells": []
                        },
                        {
                          "id": 168,
                          "name": "Ruhashya",
                          "code": "ruha",
                          "cells": []
                        },
                        {
                          "id": 169,
                          "name": "Rusatira",
                          "code": "rusati",
                          "cells": []
                        },
                        {
                          "id": 170,
                          "name": "Rwaniro",
                          "code": "rwani",
                          "cells": []
                        },
                        {
                          "id": 171,
                          "name": "Simbi",
                          "code": "simb",
                          "cells": []
                        },
                        {
                          "id": 172,
                          "name": "Tumba",
                          "code": "tumb",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 22,
                      "name": "kamonyi",
                      "code": "kam",
                      "sectors": [
                        {
                          "id": 143,
                          "name": "Cyeza",
                          "code": "cyez",
                          "cells": []
                        },
                        {
                          "id": 132,
                          "name": "Gacurambwenge",
                          "code": "gacu",
                          "cells": []
                        },
                        {
                          "id": 133,
                          "name": "Karama",
                          "code": "karam",
                          "cells": []
                        },
                        {
                          "id": 134,
                          "name": "Kayenzi",
                          "code": "kayen",
                          "cells": []
                        },
                        {
                          "id": 135,
                          "name": "Kayumbu",
                          "code": "kayum",
                          "cells": []
                        },
                        {
                          "id": 136,
                          "name": "Mugina",
                          "code": "mugin",
                          "cells": []
                        },
                        {
                          "id": 137,
                          "name": "Musambira",
                          "code": "musam",
                          "cells": []
                        },
                        {
                          "id": 138,
                          "name": "Ngamba",
                          "code": "ngamb",
                          "cells": []
                        },
                        {
                          "id": 139,
                          "name": "Nyamiyaga",
                          "code": "nyamiy",
                          "cells": []
                        },
                        {
                          "id": 140,
                          "name": "Nyarubaka",
                          "code": "nyarub",
                          "cells": []
                        },
                        {
                          "id": 141,
                          "name": "Rugalika",
                          "code": "rugal",
                          "cells": []
                        },
                        {
                          "id": 142,
                          "name": "Rukoma",
                          "code": "rukom",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 23,
                      "name": "Muhanga",
                      "code": "muh",
                      "sectors": [
                        {
                          "id": 145,
                          "name": "Kabacuzi",
                          "code": "kabac",
                          "cells": []
                        },
                        {
                          "id": 144,
                          "name": "Kibangu",
                          "code": "kiba",
                          "cells": []
                        },
                        {
                          "id": 146,
                          "name": "Kibangu",
                          "code": "kiban",
                          "cells": []
                        },
                        {
                          "id": 147,
                          "name": "Kiyumba",
                          "code": "kiyum",
                          "cells": []
                        },
                        {
                          "id": 149,
                          "name": "Mushishiro",
                          "code": "mushi",
                          "cells": []
                        },
                        {
                          "id": 148,
                          "name": "Nyabinoni",
                          "code": "nyabi",
                          "cells": []
                        },
                        {
                          "id": 150,
                          "name": "Nyarusange",
                          "code": "nyarus",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 14,
                      "name": "Nyamagabe",
                      "code": "nyam",
                      "sectors": [
                        {
                          "id": 202,
                          "name": "Gasaka",
                          "code": "gasak",
                          "cells": []
                        },
                        {
                          "id": 195,
                          "name": "Gatare",
                          "code": "gata",
                          "cells": []
                        },
                        {
                          "id": 196,
                          "name": "Kaduha",
                          "code": "kadu",
                          "cells": []
                        },
                        {
                          "id": 197,
                          "name": "Kibumbwe",
                          "code": "kibu",
                          "cells": []
                        },
                        {
                          "id": 198,
                          "name": "Kitabi",
                          "code": "kita",
                          "cells": []
                        },
                        {
                          "id": 199,
                          "name": "Musange",
                          "code": "musa",
                          "cells": []
                        },
                        {
                          "id": 200,
                          "name": "Musebeya",
                          "code": "muse",
                          "cells": []
                        },
                        {
                          "id": 201,
                          "name": "Mushubi",
                          "code": "mushu",
                          "cells": []
                        },
                        {
                          "id": 203,
                          "name": "Tare",
                          "code": "tar",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 15,
                      "name": "Nyanza",
                      "code": "nyz",
                      "sectors": [
                        {
                          "id": 158,
                          "name": "Busasamana",
                          "code": "busasa",
                          "cells": []
                        },
                        {
                          "id": 159,
                          "name": "Busoro",
                          "code": "busor",
                          "cells": []
                        },
                        {
                          "id": 160,
                          "name": "Kigoma",
                          "code": "kigom",
                          "cells": []
                        },
                        {
                          "id": 161,
                          "name": "Mukingo",
                          "code": "mukin",
                          "cells": []
                        },
                        {
                          "id": 162,
                          "name": "Muyira",
                          "code": "muyi",
                          "cells": []
                        },
                        {
                          "id": 163,
                          "name": "Ntyazo",
                          "code": "ntya",
                          "cells": []
                        },
                        {
                          "id": 164,
                          "name": "Nyagasozi",
                          "code": "nyaga",
                          "cells": []
                        },
                        {
                          "id": 165,
                          "name": "Rwabicumu",
                          "code": "rwabic",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 24,
                      "name": "Nyaruguru",
                      "code": "nyar",
                      "sectors": [
                        {
                          "id": 185,
                          "name": "Busanze",
                          "code": "busa",
                          "cells": []
                        },
                        {
                          "id": 186,
                          "name": "Cyahinda",
                          "code": "cyahi",
                          "cells": []
                        },
                        {
                          "id": 187,
                          "name": "Kibeho",
                          "code": "kibe",
                          "cells": []
                        },
                        {
                          "id": 190,
                          "name": "Kivu",
                          "code": "kiv",
                          "cells": []
                        },
                        {
                          "id": 188,
                          "name": "Mata",
                          "code": "mat",
                          "cells": []
                        },
                        {
                          "id": 192,
                          "name": "Muganza",
                          "code": "muga",
                          "cells": []
                        },
                        {
                          "id": 189,
                          "name": "Munini",
                          "code": "muni",
                          "cells": []
                        },
                        {
                          "id": 191,
                          "name": "Ngera",
                          "code": "nger",
                          "cells": []
                        },
                        {
                          "id": 193,
                          "name": "Ruramba",
                          "code": "rura",
                          "cells": []
                        },
                        {
                          "id": 194,
                          "name": "Rusenge",
                          "code": "ruse",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 25,
                      "name": "Ruhango",
                      "code": "ruh",
                      "sectors": [
                        {
                          "id": 153,
                          "name": "Bweramana",
                          "code": "bwera",
                          "cells": []
                        },
                        {
                          "id": 152,
                          "name": "Byimana",
                          "code": "byiman",
                          "cells": []
                        },
                        {
                          "id": 157,
                          "name": "Kabagari",
                          "code": "kabag",
                          "cells": []
                        },
                        {
                          "id": 151,
                          "name": "Kinazi",
                          "code": "kinaz",
                          "cells": []
                        },
                        {
                          "id": 155,
                          "name": "Kinihira",
                          "code": "kinih",
                          "cells": []
                        },
                        {
                          "id": 154,
                          "name": "Mwendo",
                          "code": "mwend",
                          "cells": []
                        },
                        {
                          "id": 156,
                          "name": "Ntongwe",
                          "code": "ntong",
                          "cells": []
                        }
                      ]
                    }
                  ]
                },
                {
                  "id": 4,
                  "name": "Western Province",
                  "code": "wp",
                  "districts": [
                    {
                      "id": 26,
                      "name": "Karongi",
                      "code": "kar",
                      "sectors": [
                        {
                          "id": 228,
                          "name": "Gitesi",
                          "code": "gite",
                          "cells": []
                        },
                        {
                          "id": 226,
                          "name": "Mubuga",
                          "code": "mubu",
                          "cells": []
                        },
                        {
                          "id": 222,
                          "name": "Rubengera",
                          "code": "rube",
                          "cells": []
                        },
                        {
                          "id": 225,
                          "name": "Rugabano",
                          "code": "rugaba",
                          "cells": []
                        },
                        {
                          "id": 224,
                          "name": "Ruganda",
                          "code": "rugan",
                          "cells": []
                        },
                        {
                          "id": 223,
                          "name": "Ruganda",
                          "code": "ruga",
                          "cells": []
                        },
                        {
                          "id": 227,
                          "name": "Rwankuba",
                          "code": "rwank",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 27,
                      "name": "Ngororero",
                      "code": "ngor",
                      "sectors": [
                        {
                          "id": 211,
                          "name": "Gatumba",
                          "code": "gatum",
                          "cells": []
                        },
                        {
                          "id": 212,
                          "name": "Hindiro",
                          "code": "hindi",
                          "cells": []
                        },
                        {
                          "id": 213,
                          "name": "Kabaya",
                          "code": "kabay",
                          "cells": []
                        },
                        {
                          "id": 214,
                          "name": "Kavumu",
                          "code": "kavum",
                          "cells": []
                        },
                        {
                          "id": 215,
                          "name": "Muhororo",
                          "code": "muhoro",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 28,
                      "name": "Nyabihu",
                      "code": "nyab",
                      "sectors": [
                        {
                          "id": 204,
                          "name": "Bigogwe",
                          "code": "bigo",
                          "cells": []
                        },
                        {
                          "id": 206,
                          "name": "Jomba",
                          "code": "jom",
                          "cells": []
                        },
                        {
                          "id": 205,
                          "name": "Kabatwa",
                          "code": "kabat",
                          "cells": []
                        },
                        {
                          "id": 207,
                          "name": "Karago",
                          "code": "karag",
                          "cells": []
                        },
                        {
                          "id": 208,
                          "name": "Mukamira",
                          "code": "mukam",
                          "cells": []
                        },
                        {
                          "id": 210,
                          "name": "Muringa",
                          "code": "muri",
                          "cells": []
                        },
                        {
                          "id": 209,
                          "name": "Rurembo",
                          "code": "rure",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 29,
                      "name": "Nyamasheke",
                      "code": "nyas",
                      "sectors": [
                        {
                          "id": 229,
                          "name": "Bushenge",
                          "code": "bushe",
                          "cells": []
                        },
                        {
                          "id": 230,
                          "name": "Cyato",
                          "code": "cya",
                          "cells": []
                        },
                        {
                          "id": 231,
                          "name": "Kagano",
                          "code": "kaga",
                          "cells": []
                        },
                        {
                          "id": 232,
                          "name": "Macuba",
                          "code": "macu",
                          "cells": []
                        },
                        {
                          "id": 234,
                          "name": "Mahembe",
                          "code": "mahe",
                          "cells": []
                        },
                        {
                          "id": 233,
                          "name": "Nyabitekeri",
                          "code": "nyabit",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 30,
                      "name": "Rubavu",
                      "code": "rub",
                      "sectors": [
                        {
                          "id": 216,
                          "name": "Bugeshi",
                          "code": "buge",
                          "cells": []
                        },
                        {
                          "id": 217,
                          "name": "Gisenyi",
                          "code": "gise",
                          "cells": []
                        },
                        {
                          "id": 218,
                          "name": "Kanzenze",
                          "code": "kanz",
                          "cells": []
                        },
                        {
                          "id": 219,
                          "name": "Mudende",
                          "code": "mudend",
                          "cells": []
                        },
                        {
                          "id": 220,
                          "name": "Nyundo",
                          "code": "nyun",
                          "cells": []
                        },
                        {
                          "id": 221,
                          "name": "Rugerero",
                          "code": "ruge",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 31,
                      "name": "Rusizi",
                      "code": "rusi",
                      "sectors": [
                        {
                          "id": 240,
                          "name": "Bugarama",
                          "code": "buga",
                          "cells": []
                        },
                        {
                          "id": 241,
                          "name": "Gashonga",
                          "code": "gasho",
                          "cells": []
                        },
                        {
                          "id": 243,
                          "name": "Giheke",
                          "code": "gihe",
                          "cells": []
                        },
                        {
                          "id": 242,
                          "name": "Gihundwe",
                          "code": "gihu",
                          "cells": []
                        },
                        {
                          "id": 246,
                          "name": "Gitambi",
                          "code": "gitam",
                          "cells": []
                        },
                        {
                          "id": 244,
                          "name": "Kamembe",
                          "code": "kame",
                          "cells": []
                        },
                        {
                          "id": 245,
                          "name": "Nkombo",
                          "code": "nkom",
                          "cells": []
                        }
                      ]
                    },
                    {
                      "id": 32,
                      "name": "Rutsiro",
                      "code": "ruts",
                      "sectors": [
                        {
                          "id": 235,
                          "name": "Boneza",
                          "code": "bone",
                          "cells": []
                        },
                        {
                          "id": 236,
                          "name": "Gihango",
                          "code": "giha",
                          "cells": []
                        },
                        {
                          "id": 237,
                          "name": "Kivumu",
                          "code": "kivum",
                          "cells": []
                        },
                        {
                          "id": 238,
                          "name": "Musasa",
                          "code": "musas",
                          "cells": []
                        },
                        {
                          "id": 239,
                          "name": "Mushubati",
                          "code": "mushub",
                          "cells": []
                        }
                      ]
                    }
                  ]
                }
              ]
        }
        """
        data = json.loads(json_data)

        for province in data['results']:
            p, _ = Province.objects.get_or_create(name=province['name'], code=province['code'])
            for district in province['districts']:
                d, _ = District.objects.get_or_create(name=district['name'], code=district['code'], province=p)
                for sector in district['sectors']:
                    s, _ = Sector.objects.get_or_create(name=sector['name'], code=sector['code'], district=d)
                    for cell in sector['cells']:
                        c, _ = Cell.objects.get_or_create(name=cell['name'], code=cell['code'], sector=s)
                        for village in cell.get('villages', []):
                            Village.objects.get_or_create(name=village['name'], code=village['code'], cell=c)
        self.stdout.write(self.style.SUCCESS("Locations imported successfully."))
