# Datasets

## Notice

Since there is no free lunch, we only provide the public dataset for this open source.

The Customer's Rating Data used in GeoCommend Model is scraped from the internet with our web-crawler script, so you won't get it for free here, unless you want pay us for it.

## Description

### Location Data for selected fast food brands

| Brand | File |
|----------|-----------|
| Yoshinoya | [yoshinoya.json](yoshinoya.json) |
| McDonald's | [mcdonalds.json](mcdonalds.json) |
| KFC | [kfc.json](kfc.json) |
| Fairwood | [fairwood.json](fairwood.json) |
| Cafe de Coral | [cdc.json](cdc.json) |

These datasets record the latitude and longitude of each store of the brand. Some of them also record type of the store.

### Demographic Public Dataset

These datasets also from CSDI, thanks to them for providing these data for free. The description of each dataset can be found in the CSDI website.

| Dataset | File |
|----------|-----------|
| Public Market in HK | [PMRK.geojson](PMRK.geojson) |
| Demographic Data in HK | [DCCA_21C.geojson](DCCA_21C.geojson) |
| Rental Data in HK | [Shop_and_Other_Commercial_Assessments.geojson](Shop_and_Other_Commercial_Assessments.geojson) |

### MTR Station Data

[MTRStations.json](MTRStations.json)

which includes the latitude and longitude of each MTR station in Hong Kong.

We also provide a script to scrape the data from the Wiki, which is [`MTRStationScraper.py`](../code/MTRStationScraper.py).