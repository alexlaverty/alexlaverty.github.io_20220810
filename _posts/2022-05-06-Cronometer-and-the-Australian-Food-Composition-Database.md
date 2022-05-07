---
layout: post
title: Cronometer and the Australian Food Composition Database
description: Article Description
date: 2022-05-01
categories: [nutrition, tech]
image:
  src: /assets/img/nutrition/thumbnail.png
hide_thumbnail: False
---

I thought I would have a play around with the [Australian Food Composition Database](https://www.foodstandards.gov.au/science/monitoringnutrients/afcd/Pages/default.aspx) which contains a spreadsheet of foods and their vitamin and mineral amounts. 

The spreadsheet can be downloaded here :
<https://www.foodstandards.gov.au/science/monitoringnutrients/afcd/Pages/downloadableexcelfiles.aspx>

I used [Python](https://www.python.org/) and my favourite library [Pandas](https://pandas.pydata.org/) to read in the spreadsheet file :


```
spreadsheet_name = "Release 2 - Nutrient file.xlsx"
df = pd.read_excel(spreadsheet_name, sheet_name=1)
```

The first thing I noticed with the spreadsheet is the column headers have a newline in them which would making it difficult to select so I removed the new line in the header columns :

```
df.columns = [x.replace("\n", "") for x in df.columns.to_list()]
```

There were quite a few columns apparently 293 in total :

```
print(df.shape[1])
293
```

I wanted to print out a list of the column headers, some of them I wasn't interested in or didn't know what they were so I used regex to exclude them :

```
for col in df.columns:
    matchObj = re.search("(C\d.*|Energy.*|Total.*|25-hydroxy.*|.*tocopherol)", col)
    if not matchObj:
        print(col)
```
 
list of column headers to choose from :

```
Public Food Key
Classification
Food Name
Moisture (water) (g)
Protein (g)
Nitrogen (g)
Fat, total (g)
Ash (g)
Alcohol (g)
Fructose (g)
Glucose (g)
Sucrose(g)
Maltose (g)
Lactose (g)
Galactose (g)
Maltotrios (g)
Added sugars (g)
Free sugars (g)
Starch (g)
Dextrin (g)
Glycerol (g)
Glycogen (g)
Inulin (g)
Erythritol (g)
Maltitol (g)
Mannitol (g)
Xylitol (g)
Maltodextrin (g)
Oligosaccharides  (g)
Polydextrose (g)
Raffinose (g)
Stachyose (g)
Sorbitol (g)
Resistant starch (g)
Available carbohydrate, without sugar alcohols (g)
Available carbohydrate, with sugar alcohols (g)
Acetic acid (g)
Citric acid (g)
Fumaric acid (g)
Lactic acid (g)
Malic acid (g)
Oxalic acid (g)
Propionic acid (g)
Quinic acid (g)
Shikimic acid (g)
Succinic acid (g)
Tartaric acid (g)
Aluminium (Al) (ug)
Antimony (Sb) (ug)
Arsenic (As) (ug)
Cadmium (Cd) (ug)
Calcium (Ca) (mg)
Chromium (Cr) (ug)
Chloride (Cl) (mg)
Cobalt (Co) (ug)
Copper (Cu) (mg)
Fluoride (F) (ug)
Iodine (I) (ug)
Iron (Fe) (mg)
Lead (Pb) (ug)
Magnesium (Mg) (mg)
Manganese (Mn) (mg)
Mercury (Hg) (ug)
Molybdenum (Mo) (ug)
Nickel (Ni) (ug)
Phosphorus (P) (mg)
Potassium (K) (mg)
Selenium (Se) (ug)
Sodium (Na) (mg)
Sulphur (S) (mg)
Tin (Sn) (ug)
Zinc (Zn) (mg)
Retinol (preformed vitamin A) (ug)
Alpha-carotene (ug)
Beta-carotene (ug)
Cryptoxanthin (ug)
Beta-carotene equivalents (provitamin A) (ug)
Vitamin A retinol equivalents (ug)
Lutein (ug)
Lycopene (ug)
Xanthophyl (ug)
Thiamin (B1) (mg)
Riboflavin (B2) (mg)
Niacin (B3) (mg)
Niacin derived from tryptophan (mg)
Niacin derived equivalents (mg)
Pantothenic acid (B5) (mg)
Pyridoxine (B6) (mg)
Biotin (B7) (ug)
Cobalamin (B12) (ug)
Folate, natural (ug)
Folic acid (ug)
Dietary folate equivalents (ug)
Vitamin C (mg)
Cholecalciferol (D3) (ug)
Ergocalciferol (D2) (ug)
Vitamin D3 equivalents (ug)
Alpha tocotrienol (mg)
Beta tocotrienol (mg)
Delta tocotrienol (mg)
Gamma tocotrienol (mg)
Vitamin E (mg)
Caffeine (mg)
Cholesterol (mg)
Alanine (mg/gN)
Arginine (mg/gN)
Aspartic acid (mg/gN)
Cystine plus cysteine (mg/gN)
Glutamic acid (mg/gN)
Glycine (mg/gN)
Histidine (mg/gN)
Isoleucine (mg/gN)
Leucine (mg/gN)
Lysine (mg/gN)
Methionine (mg/gN)
Phenylalanine (mg/gN)
Proline (mg/gN)
Serine (mg/gN)
Threonine (mg/gN)
Tyrosine (mg/gN)
Tryptophan (mg/gN)
Valine (mg/gN)
Alanine (mg)
Arginine (mg)
Aspartic acid (mg)
Cystine plus cysteine (mg)
Glutamic acid (mg)
Glycine (mg)
Histidine (mg)
Isoleucine (mg)
Leucine (mg)
Lysine (mg)
Methionine (mg)
Phenylalanine (mg)
Proline (mg)
Serine (mg)
Threonine (mg)
Tyrosine (mg)
Tryptophan (mg)
Valine (mg)
```

I decided to just focus on the essential micronutrients and came up with this list :

```
micronutrients = [
                    'Biotin (B7) (ug)',
                    'Calcium (Ca) (mg)',
                    'Chloride (Cl) (mg)',
                    'Chromium (Cr) (ug)',
                    'Cobalamin (B12) (ug)',
                    'Cobalt (Co) (ug)',
                    'Copper (Cu) (mg)',
                    'Fluoride (F) (ug)',
                    'Folic acid (ug)',
                    'Iodine (I) (ug)',
                    'Iron (Fe) (mg)',
                    'Magnesium (Mg) (mg)',
                    'Manganese (Mn) (mg)',
                    'Niacin (B3) (mg)',
                    'Pantothenic acid (B5) (mg)',
                    'Phosphorus (P) (mg)',
                    'Phosphorus (P) (mg)',
                    'Potassium (K) (mg)',
                    'Pyridoxine (B6) (mg)',
                    'Riboflavin (B2) (mg)',
                    'Selenium (Se) (ug)',
                    'Thiamin (B1) (mg)',
                    'Vitamin A retinol equivalents (ug)',
                    'Vitamin C (mg)',
                    'Vitamin D3 equivalents (ug)',
                    'Vitamin E (mg)',
                    'Zinc (Zn) (mg)'
                ]
```

From there I wanted to loop through each micronutrient and get the top 10 foods and print it out :

```
column_names = ["foodname","value","micronutrient"]
top_foods = pd.DataFrame(columns=column_names)

for micronutrient in micronutrients :
    foods = df[['Food Name', micronutrient]].sort_values(micronutrient, ascending=False).head(10)
    foods['micronutrient'] = micronutrient
    foods.columns = column_names
    top_foods = pd.concat([top_foods, foods])

print(top_foods[["micronutrient","foodname","value"]].sort_values(["micronutrient","value"], ascending=[True,False]))
```

If you see foods in the list that you don't like you can drop those foods from the dataframe for example :

```
exclude_foods = ['Abalone','liver','Milk','wheat','Mutton','Dairy','Wheat']

df = df[df["Food Name"].str.contains("|".join(exclude_foods))==False]
```

The Top 10 Foods for each essential micronutrient from the Australian Food Composition Database as of todays date `07/05/2022` looks like this :

```
PS D:\src\nutrient-data> python .\app.py

                           micronutrient                                           foodname    value
31                      Biotin (B7) (ug)                                  Yeast, dry powder    200.0
1187                    Biotin (B7) (ug)  Nut, peanut, with skin, roasted, with oil, salted    130.0
1188                    Biotin (B7) (ug)  Nut, peanut, without skin, roasted, with oil, ...    100.0
70                      Biotin (B7) (ug)  Coffee, instant, dry powder or granules, decaf...    100.0
68                      Biotin (B7) (ug)            Coffee, instant, dry powder or granules    100.0
1189                    Biotin (B7) (ug)  Nut, peanut, without skin, roasted, with oil, ...    100.0
1186                    Biotin (B7) (ug)              Nut, peanut, with skin, raw, unsalted     88.0
1184                    Biotin (B7) (ug)                       Nut, hazelnut, raw, unsalted     79.0
1177                    Biotin (B7) (ug)                                   Nut, almond meal     56.0
1358                    Biotin (B7) (ug)            Confectionery, peanut, chocolate-coated     46.5

16                     Calcium (Ca) (mg)                               Thyme, dried, ground     1890
15                     Calcium (Ca) (mg)                                        Sage, dried     1652
11                     Calcium (Ca) (mg)                                     Oregano, dried     1597
1197                   Calcium (Ca) (mg)                                        Seed, poppy     1438
388                    Calcium (Ca) (mg)                                      Paste, shrimp     1380
14                     Calcium (Ca) (mg)                                    Rosemary, dried     1280
462                    Calcium (Ca) (mg)                            Milk, cow, powder, skim     1100
2                      Calcium (Ca) (mg)                            Cinnamon, dried, ground     1002
424                    Calcium (Ca) (mg)  Cheese, cheddar, natural, reduced fat (approxi...      995
435                    Calcium (Ca) (mg)             Cheese, parmesan, dried, finely grated      970

20                    Chloride (Cl) (mg)                           Salt, table, non-iodised  61200.0
19                    Chloride (Cl) (mg)                               Salt, table, iodised  61200.0
21                    Chloride (Cl) (mg)                          Stock, dry powder or cube  32100.0
22                    Chloride (Cl) (mg)                   Taco seasoning mix, chilli-based  14000.0
1341                  Chloride (Cl) (mg)                   Soup, vegetable, instant dry mix  11400.0
1337                  Chloride (Cl) (mg)      Soup, broth style, with meat, instant dry mix  11100.0
379                   Chloride (Cl) (mg)                              Gravy powder, dry mix  10900.0
406                   Chloride (Cl) (mg)                             Sauce, soy, commercial  10100.0
407                   Chloride (Cl) (mg)               Sauce, soy, commercial, reduced salt  10100.0
1338                  Chloride (Cl) (mg)  Soup, broth style, with meat & noodles, instan...   7760.0

1277                  Chromium (Cr) (ug)              Abalone, black lip, aquacultured, raw    392.5
1279                  Chromium (Cr) (ug)              Abalone, green lip, aquacultured, raw    293.3
1281                  Chromium (Cr) (ug)                      Abalone, brown lip, wild, raw    265.0
1280                  Chromium (Cr) (ug)                      Abalone, green lip, wild, raw    168.2
1262                  Chromium (Cr) (ug)  Trout, ocean, aquacultured, fillet, without sk...    162.7
1278                  Chromium (Cr) (ug)                      Abalone, black lip, wild, raw    142.0
1263                  Chromium (Cr) (ug)  Trout, ocean, aquacultured, fillet, without sk...    141.4
1194                  Chromium (Cr) (ug)                                 Psyllium, uncooked    120.0
1261                  Chromium (Cr) (ug)  Trout, ocean, aquacultured, fillet, without sk...    118.8
153                   Chromium (Cr) (ug)                            Bread, from white flour     69.7

1137                Cobalamin (B12) (ug)                 Lamb, liver, grilled, no added fat     76.5
1285                Cobalamin (B12) (ug)                              Mussel, blue, steamed     20.0
1286                Cobalamin (B12) (ug)                                       Octopus, raw     20.0
1287                Cobalamin (B12) (ug)                      Octopus, boiled, no added fat     17.8
1135                Cobalamin (B12) (ug)                                Chicken, liver, raw     16.6
1136                Cobalamin (B12) (ug)                Chicken, liver, fried, added butter     15.8
1279                Cobalamin (B12) (ug)              Abalone, green lip, aquacultured, raw     15.0
1277                Cobalamin (B12) (ug)              Abalone, black lip, aquacultured, raw     15.0
1288                Cobalamin (B12) (ug)                  Oyster, native, aquacultured, raw     15.0
1281                Cobalamin (B12) (ug)                      Abalone, brown lip, wild, raw     15.0

1205                    Cobalt (Co) (ug)                                 Bassa, fillet, raw      1.0
1206                    Cobalt (Co) (ug)          Bassa (basa), fillet, baked, no added fat      1.0
1207                    Cobalt (Co) (ug)        Bassa (basa), fillet, steamed, no added fat      1.0
110                     Cobalt (Co) (ug)                                         Water, tap      0.0
1240                    Cobalt (Co) (ug)    Salmon, Atlantic, fillet, steamed, no added fat      0.0
1265                    Cobalt (Co) (ug)  Trout, rainbow, aquacultured, baked, no added fat      0.0
1264                    Cobalt (Co) (ug)                  Trout, rainbow, aquacultured, raw      0.0
1260                    Cobalt (Co) (ug)             Tilapia, fillet, steamed, no added fat      0.0
1259                    Cobalt (Co) (ug)               Tilapia, fillet, baked, no added fat      0.0
1258                    Cobalt (Co) (ug)                               Tilapia, fillet, raw      0.0

262                     Copper (Cu) (mg)                                   Bulgur, uncooked     17.0
140                     Copper (Cu) (mg)                   Cone, wafer style, for ice cream      8.7
1137                    Copper (Cu) (mg)                 Lamb, liver, grilled, no added fat      8.1
61                      Copper (Cu) (mg)                                       Cocoa powder      3.7
1180                    Copper (Cu) (mg)                     Nut, cashew, roasted, unsalted      2.2
1178                    Copper (Cu) (mg)             Nut, brazil, raw or blanched, unsalted      2.0
1199                    Copper (Cu) (mg)                                    Seed, sunflower      2.0
1181                    Copper (Cu) (mg)                       Nut, cashew, roasted, salted      2.0
1179                    Copper (Cu) (mg)                         Nut, cashew, raw, unsalted      1.9
1295                    Copper (Cu) (mg)  Prawn, black tiger, aquacultured, purchased co...    1.808

26                     Fluoride (F) (ug)                                Gelatine, all types   6500.0
1093                   Fluoride (F) (ug)               Turkey, hindquarter, lean flesh, raw   1600.0
1233                   Fluoride (F) (ug)     Mullet, yelloweye, fillet, baked, no added fat  1356.16
1095                   Fluoride (F) (ug)   Turkey, hindquarter, lean flesh, skin & fat, raw   1353.0
1104                   Fluoride (F) (ug)  Duck, lean flesh, skin & fat, baked, no added fat  1056.41
1101                   Fluoride (F) (ug)                              Duck, skin & fat, raw   1000.0
1134                   Fluoride (F) (ug)            Rabbit, flesh, casseroled, no added fat   1000.0
1232                   Fluoride (F) (ug)                     Mullet, yelloweye, fillet, raw    990.0
1102                   Fluoride (F) (ug)              Duck, skin & fat, baked, no added fat    900.0
1215                   Fluoride (F) (ug)               Flathead, flesh, baked, no added fat   890.41

417                      Folic acid (ug)                            Spread, yeast, vegemite     2354
416                      Folic acid (ug)                             Spread, yeast, marmite     1500
209                      Folic acid (ug)  Breakfast cereal, puffed or popped rice, cocoa...     1056
203                      Folic acid (ug)  Breakfast cereal, mixed grain (rice & wheat), ...      910
204                      Folic acid (ug)  Breakfast cereal, mixed grain (wheat & oat), f...      592
215                      Folic acid (ug)  Breakfast cereal, whole wheat, flakes, dried f...      351
210                      Folic acid (ug)  Breakfast cereal, wheat bran, flakes, sultanas...      335
202                      Folic acid (ug)  Breakfast cereal, flakes of corn, added vitami...      335
141                      Folic acid (ug)                                 Breadcrumbs, white      261
214                      Folic acid (ug)  Breakfast cereal, whole wheat, biscuit, added ...      246

19                       Iodine (I) (ug)                               Salt, table, iodised   4400.0
1568                     Iodine (I) (ug)                               Seaweed, nori, dried   2200.0
1569                     Iodine (I) (ug)                           Seaweed, boiled, drained    337.2
1285                     Iodine (I) (ug)                              Mussel, blue, steamed    267.8
59                       Iodine (I) (ug)  Protein powder, whey based, protein >70%, unfo...    240.0
1289                     Iodine (I) (ug)                 Oyster, Pacific, aquacultured, raw    202.0
1279                     Iodine (I) (ug)              Abalone, green lip, aquacultured, raw    201.7
462                      Iodine (I) (ug)                            Milk, cow, powder, skim    200.0
1280                     Iodine (I) (ug)                      Abalone, green lip, wild, raw    190.0
1291                     Iodine (I) (ug)                          Oyster, aquacultured, raw    183.8

16                        Iron (Fe) (mg)                               Thyme, dried, ground    123.6
5                         Iron (Fe) (mg)                 Cumin (cummin) seed, dried, ground    66.36
17                        Iron (Fe) (mg)                            Turmeric, dried, ground     55.0
416                       Iron (Fe) (mg)                             Spread, yeast, marmite     46.3
11                        Iron (Fe) (mg)                                     Oregano, dried     36.8
7                         Iron (Fe) (mg)                              Fenugreek seed, dried    33.53
61                        Iron (Fe) (mg)                                       Cocoa powder     30.0
14                        Iron (Fe) (mg)                                    Rosemary, dried    29.25
15                        Iron (Fe) (mg)                                        Sage, dried    28.12
1194                      Iron (Fe) (mg)                                 Psyllium, uncooked     24.0

61                   Magnesium (Mg) (mg)                                       Cocoa powder      590
1198                 Magnesium (Mg) (mg)                      Seed, pumpkin, hulled & dried      530
293                  Magnesium (Mg) (mg)                  Wheat bran, unprocessed, uncooked      450
15                   Magnesium (Mg) (mg)                                        Sage, dried      428
1195                 Magnesium (Mg) (mg)                                  Seed, chia, dried      380
1199                 Magnesium (Mg) (mg)                                    Seed, sunflower      370
5                    Magnesium (Mg) (mg)                 Cumin (cummin) seed, dried, ground      366
128                  Magnesium (Mg) (mg)                       Biscuit, savoury, seed based      350
1178                 Magnesium (Mg) (mg)             Nut, brazil, raw or blanched, unsalted      350
1197                 Magnesium (Mg) (mg)                                        Seed, poppy      347

1279                 Manganese (Mn) (mg)              Abalone, green lip, aquacultured, raw     33.5
1284                 Manganese (Mn) (mg)  Lobster, southern rock, wild, flesh, purchased...   26.562
1283                 Manganese (Mn) (mg)           Lobster, southern rock, wild, flesh, raw   23.906
1280                 Manganese (Mn) (mg)                      Abalone, green lip, wild, raw     18.0
294                  Manganese (Mn) (mg)                                         Wheat germ     16.0
211                  Manganese (Mn) (mg)  Breakfast cereal, wheat bran, pellets, added v...     11.5
1191                 Manganese (Mn) (mg)                           Nut, pine, raw, unsalted      6.9
212                  Manganese (Mn) (mg)  Breakfast cereal, whole wheat, biscuit, bran, ...      6.4
210                  Manganese (Mn) (mg)  Breakfast cereal, wheat bran, flakes, sultanas...     5.29
1185                 Manganese (Mn) (mg)                      Nut, macadamia, raw, unsalted      5.1

417                     Niacin (B3) (mg)                            Spread, yeast, vegemite    124.0
416                     Niacin (B3) (mg)                             Spread, yeast, marmite     50.0
31                      Niacin (B3) (mg)                                  Yeast, dry powder     28.0
70                      Niacin (B3) (mg)  Coffee, instant, dry powder or granules, decaf...     25.0
68                      Niacin (B3) (mg)            Coffee, instant, dry powder or granules     25.0
293                     Niacin (B3) (mg)                  Wheat bran, unprocessed, uncooked     19.0
1187                    Niacin (B3) (mg)  Nut, peanut, with skin, roasted, with oil, salted     18.0
1189                    Niacin (B3) (mg)  Nut, peanut, without skin, roasted, with oil, ...     18.0
1188                    Niacin (B3) (mg)  Nut, peanut, without skin, roasted, with oil, ...     18.0
1054                    Niacin (B3) (mg)   Chicken, breast, lean flesh, fried, no added fat    16.73

1137          Pantothenic acid (B5) (mg)                 Lamb, liver, grilled, no added fat      7.0
1136          Pantothenic acid (B5) (mg)                Chicken, liver, fried, added butter     5.94
546           Pantothenic acid (B5) (mg)                            Egg, chicken, yolk, raw      5.2
1135          Pantothenic acid (B5) (mg)                                Chicken, liver, raw      5.0
417           Pantothenic acid (B5) (mg)                            Spread, yeast, vegemite      4.6
31            Pantothenic acid (B5) (mg)                                  Yeast, dry powder      4.3
1186          Pantothenic acid (B5) (mg)              Nut, peanut, with skin, raw, unsalted      3.6
1188          Pantothenic acid (B5) (mg)  Nut, peanut, without skin, roasted, with oil, ...      3.4
1189          Pantothenic acid (B5) (mg)  Nut, peanut, without skin, roasted, with oil, ...      3.4
1187          Pantothenic acid (B5) (mg)  Nut, peanut, with skin, roasted, with oil, salted      3.3

1198                 Phosphorus (P) (mg)                      Seed, pumpkin, hulled & dried     1100
462                  Phosphorus (P) (mg)                            Milk, cow, powder, skim     1000
293                  Phosphorus (P) (mg)                  Wheat bran, unprocessed, uncooked     1000
417                  Phosphorus (P) (mg)                            Spread, yeast, vegemite      880
319                  Phosphorus (P) (mg)              Flour, wheat, wholemeal, self-raising      874
1197                 Phosphorus (P) (mg)                                        Seed, poppy      870
31                   Phosphorus (P) (mg)                                  Yeast, dry powder      860
1195                 Phosphorus (P) (mg)                                  Seed, chia, dried      830
460                  Phosphorus (P) (mg)        Milk, cow, powder, regular fat, unfortified      810
461                  Phosphorus (P) (mg)  Milk, cow, powder, regular fat, added vitamins...      810

18                    Potassium (K) (mg)                Salt substitute, potassium chloride    50009
25                    Potassium (K) (mg)                        Cream of tartar, dry powder    16500
23                    Potassium (K) (mg)                          Baking powder, dry powder     8267
61                    Potassium (K) (mg)                                       Cocoa powder     4400
68                    Potassium (K) (mg)            Coffee, instant, dry powder or granules     3500
70                    Potassium (K) (mg)  Coffee, instant, dry powder or granules, decaf...     3500
1604                  Potassium (K) (mg)                                   Tomato, sundried     3170
1568                  Potassium (K) (mg)                               Seaweed, nori, dried     2900
12                    Potassium (K) (mg)                                Paprika, dry powder     2280
417                   Potassium (K) (mg)                            Spread, yeast, vegemite     2122

15                  Pyridoxine (B6) (mg)                                        Sage, dried     2.69
685                 Pyridoxine (B6) (mg)                                    Chickpea, dried      2.6
307                 Pyridoxine (B6) (mg)                            Flour, chickpea (besan)      2.6
100                 Pyridoxine (B6) (mg)                        Soft drink, energy drink, V      2.5
99                  Pyridoxine (B6) (mg)                 Soft drink, energy drink, Red Bull     2.27
12                  Pyridoxine (B6) (mg)                                Paprika, dry powder     2.14
1                   Pyridoxine (B6) (mg)                      Chilli (chili), dried, ground     2.09
1602                Pyridoxine (B6) (mg)                       Tomato, paste, no added salt     2.04
1601                Pyridoxine (B6) (mg)                     Tomato, paste, with added salt     2.03
62                  Pyridoxine (B6) (mg)  Beverage base, chocolate flavour, added vitami...      2.0

417                 Riboflavin (B2) (mg)                            Spread, yeast, vegemite   17.111
416                 Riboflavin (B2) (mg)                             Spread, yeast, marmite      8.4
1137                Riboflavin (B2) (mg)                 Lamb, liver, grilled, no added fat      4.5
1324                Riboflavin (B2) (mg)                    Bar, snack, fruit filled, baked     1.91
1136                Riboflavin (B2) (mg)                Chicken, liver, fried, added butter    1.903
208                 Riboflavin (B2) (mg)  Breakfast cereal, puffed or popped rice, added...      1.9
203                 Riboflavin (B2) (mg)  Breakfast cereal, mixed grain (rice & wheat), ...    1.832
205                 Riboflavin (B2) (mg)  Breakfast cereal, mixed grain (wheat, oat & co...      1.8
1135                Riboflavin (B2) (mg)                                Chicken, liver, raw    1.778
62                  Riboflavin (B2) (mg)  Beverage base, chocolate flavour, added vitami...    1.762

1178                  Selenium (Se) (ug)             Nut, brazil, raw or blanched, unsalted   1917.0
9                     Selenium (Se) (ug)                                     Mustard powder    160.0
1234                  Selenium (Se) (ug)   Mullet, yelloweye, fillet, steamed, no added fat    110.0
1233                  Selenium (Se) (ug)     Mullet, yelloweye, fillet, baked, no added fat     98.6
1245                  Selenium (Se) (ug)    Sardine, Australian, whole, fried, no added fat     97.4
1247                  Selenium (Se) (ug)  Sprat, blue, wild caught, flesh, skin & bones,...     97.4
1244                  Selenium (Se) (ug)                    Sardine, Australian, whole, raw     97.0
1285                  Selenium (Se) (ug)                              Mussel, blue, steamed     96.0
1219                  Selenium (Se) (ug)              Gemfish, flesh, steamed, no added fat     84.6
1246                  Selenium (Se) (ug)  Sprat, blue, wild caught, flesh, skin & bones,...     82.8

417                    Thiamin (B1) (mg)                            Spread, yeast, vegemite   22.778
416                    Thiamin (B1) (mg)                             Spread, yeast, marmite     11.0
404                    Thiamin (B1) (mg)              Sauce, simmer for chicken, commercial      2.8
205                    Thiamin (B1) (mg)  Breakfast cereal, mixed grain (wheat, oat & co...      2.8
214                    Thiamin (B1) (mg)  Breakfast cereal, whole wheat, biscuit, added ...    2.567
976                    Thiamin (B1) (mg)                            Pork, fillet, lean, raw      1.5
977                    Thiamin (B1) (mg)   Pork, fillet, fully-trimmed, baked, no added fat      1.5
294                    Thiamin (B1) (mg)                                         Wheat germ      1.5
208                    Thiamin (B1) (mg)  Breakfast cereal, puffed or popped rice, added...      1.4
971                    Thiamin (B1) (mg)  Pork, butterfly steak, lean, grilled, no added...      1.4

1137  Vitamin A retinol equivalents (ug)                 Lamb, liver, grilled, no added fat    31007
1135  Vitamin A retinol equivalents (ug)                                Chicken, liver, raw    12007
1136  Vitamin A retinol equivalents (ug)                Chicken, liver, fried, added butter    10726
12    Vitamin A retinol equivalents (ug)                                Paprika, dry powder     4360
1     Vitamin A retinol equivalents (ug)                      Chilli (chili), dried, ground     2500
1439  Vitamin A retinol equivalents (ug)  Carrot, mature, peeled, fresh, baked, no added...     1971
1438  Vitamin A retinol equivalents (ug)                 Carrot, mature, peeled, fresh, raw     1701
1440  Vitamin A retinol equivalents (ug)     Carrot, mature, peeled, fresh, boiled, drained     1682
1437  Vitamin A retinol equivalents (ug)                  Carrot, baby, baked, no added fat     1674
1435  Vitamin A retinol equivalents (ug)                   Carrot, baby, peeled, fresh, raw     1622

669                       Vitamin C (mg)                                Lime, native, fruit      347
1433                      Vitamin C (mg)                          Capsicum, red, fresh, raw      330
1434                      Vitamin C (mg)          Capsicum, red, fresh, fried, no added fat      312
1568                      Vitamin C (mg)                               Seaweed, nori, dried      290
593                       Vitamin C (mg)                               Guava, Hawaiian, raw      243
1431                      Vitamin C (mg)                        Capsicum, green, fresh, raw      220
1432                      Vitamin C (mg)        Capsicum, green, fresh, fried, no added fat      208
1457                      Vitamin C (mg)                           Chilli (chili), red, raw      201
1458                      Vitamin C (mg)           Chilli (chili), red, fried, no added fat      190
1514                      Vitamin C (mg)                   Parsley, continental, fresh, raw      180

1502         Vitamin D3 equivalents (ug)  Mushroom, common, vitamin D enhanced, fresh, f...    38.86
1501         Vitamin D3 equivalents (ug)   Mushroom, common, vitamin D enhanced, fresh, raw    24.18
546          Vitamin D3 equivalents (ug)                            Egg, chicken, yolk, raw     17.0
547          Vitamin D3 equivalents (ug)                    Egg, chicken, yolk, hard-boiled     17.0
62           Vitamin D3 equivalents (ug)  Beverage base, chocolate flavour, added vitami...     13.5
1203         Vitamin D3 equivalents (ug)  Barramundi, aquacultured, fillet, grilled, no ...    13.19
1202         Vitamin D3 equivalents (ug)              Barramundi, aquacultured, fillet, raw     10.7
1312         Vitamin D3 equivalents (ug)              Salmon, red, canned in brine, drained     10.6
1311         Vitamin D3 equivalents (ug)               Salmon, flavoured, canned, undrained     10.6
1310         Vitamin D3 equivalents (ug)             Salmon, pink, canned in brine, drained     10.6

1200                      Vitamin E (mg)                           Tahini, sesame seed pulp    211.0
533                       Vitamin E (mg)                                     Oil, sunflower     56.1
1199                      Vitamin E (mg)                                    Seed, sunflower    41.21
1                         Vitamin E (mg)                      Chilli (chili), dried, ground    38.14
522                       Vitamin E (mg)                                    Oil, cottonseed     35.3
509                       Vitamin E (mg)        Margarine spread, polyunsaturated (70% fat)    34.68
531                       Vitamin E (mg)                                     Oil, rice bran     32.3
1175                      Vitamin E (mg)              Nut, almond, with skin, raw, unsalted    31.42
12                        Vitamin E (mg)                                Paprika, dry powder     29.1
1176                      Vitamin E (mg)          Nut, almond, with skin, roasted, unsalted    28.58

1290                      Zinc (Zn) (mg)             Oyster, Sydney rock, aquacultured, raw    20.25
1289                      Zinc (Zn) (mg)                 Oyster, Pacific, aquacultured, raw    18.04
31                        Zinc (Zn) (mg)                                  Yeast, dry powder     18.0
1291                      Zinc (Zn) (mg)                          Oyster, aquacultured, raw    17.37
1604                      Zinc (Zn) (mg)                                   Tomato, sundried     13.6
1288                      Zinc (Zn) (mg)                  Oyster, native, aquacultured, raw    11.05
929                       Zinc (Zn) (mg)  Lamb, with bone, shin, lean, casseroled, no ad...     10.0
931                       Zinc (Zn) (mg)  Lamb, with bone, shin, semi-trimmed, casserole...     9.41
943                       Zinc (Zn) (mg)  Mutton, boneless dice or strips, shoulder, lea...      8.9
945                       Zinc (Zn) (mg)  Mutton, boneless dice or strips, shoulder, sem...     8.76
```

The funny thing is if take the above list and group them by name and get a count and sort it, the food that occurs the most in this list is Vegemite :

<img src="/assets/img/nutrition/vegemite.png">

Here is the Top 10 Foods that occur in the above table :

```
df2 = top_foods.groupby(['foodname'])['foodname'].count().sort_values(ascending=False) 
print(df2.head(10))

foodname
Spread, yeast, vegemite                  8
Yeast, dry powder                        6
Spread, yeast, marmite                   5
Lamb, liver, grilled, no added fat       5
Chicken, liver, raw                      4
Wheat bran, unprocessed, uncooked        4
Chicken, liver, fried, added butter      4
Abalone, green lip, aquacultured, raw    4
Paprika, dry powder                      4
Milk, cow, powder, skim                  4
```

So maybe I need to go and read up a bit more on Vegemite.... this website says the following :

<https://firstthingsfirst.com.au/Blog/Is-Vegemite-good-for-you>

>"packed with B vitamins, containing a great big dollop of niacin, riboflavin and thiamine. It also has 50 percent of the recommended daily intake for folate. You’ll also get a good dose of calcium, magnesium, potassium, iron and selenium. These vitamins are known to help keep the skin and eyes healthy, improve cell health, boost the digestive system and keep your nerves in check."

Next I then went to a diet tracker called Cronometer which allows you to track calories, fat, protein etc like a normal diet tracker does but in addition it also allows you to track vitamin and mineral content in foods :

<https://cronometer.com/>

I added in one of the top sources of each micronutrient into cronometer, once I'd added each food into cronometer it ended up looking like this :

<a href="/assets/img/nutrition/cronometer.com.png"><img src="/assets/img/nutrition/cronometer.com.png"></a>

At a quick glance the day of eating consists of Seafood, nuts, herbs and vegetables. I'm sure that one could easily make some kind of mediterranean dish using these ingredients.

Side note, I found a cool little shortcut in Chrome browser which will take a full screenshot of a website, which is how I took the above screenshot :

```
* Press Ctrl-Shift-I (or Cmd-Option-I on a Mac).
* Press Ctrl-Shift-P (or Cmd-Shift-P on a Mac).
* Type the word screenshot.
```

So if you wanted a super nutrient dense healthy meal plan this is one way to approach it from a data driven perspective.

For future improvements I would like to try scraping this nutritional database and then passing the foods into these machine learning algorithms to optimize the amounts of each ingredient :

<http://inductivebias.com/Blog/project-auto-soylent/>

<https://gist.github.com/jstorry/6521537a9a4f759ebfc8>

<https://github.com/nick/auto-soylent>

<https://machinelearninggeek.com/solving-balanced-diet-problem-in-python-using-pulp/>

<https://www.completefoods.co/diy/genetic-soylent>

That way you wouldn't have to sit there manually tweaking amounts in cronometer to get the optimal amounts for each food it would generate it for you, but that might be a project for another day : )