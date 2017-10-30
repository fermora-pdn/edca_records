import ocdsmerge
import pprint
import json
import datetime
import os
import sys
import getopt
import codecs
from pymongo import MongoClient

def main(argv):
    output = ''
    try:
        opts, args = getopt.getopt(argv, "ho:", ["otype="])
    except getopt.GetoptError:
        print ('merge.py -o <output_type>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -o <output_type>')
            sys.exit()
        elif opt in ("-o", "--otype"):
            output = arg

    # Mongo db config
    client = MongoClient('localhost', 27017)
    db = client.EDCA
    collection = db.Releases

    output_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "output")
    # print(output_dir)

    #for ocid in collection.distinct("ocid"):
    for cp in collection.aggregate([{"$group": {"_id": "$ocid", "conteo": {"$sum": 1 }}}]):
        ocid = cp["_id"]
        # print('Processing -> ', ocid)

        recordPackage = {}
        recordPackage["uri"] = "https://api.datos.gob.mx/v1/"
        recordPackage["version"] = "1.1"
        recordPackage["extensions"] = [
            "https://raw.githubusercontent.com/open-contracting/ocds_location_extension/v1.1.1/extension.json",
            "https://raw.githubusercontent.com/open-contracting/ocds_additionalContactPoints_extension/master/extension.json",
            "https://raw.githubusercontent.com/open-contracting/ocds_budget_breakdown_extension/master/extension.json",
            "https://raw.githubusercontent.com/open-contracting/ocds_contract_suppliers_extension/master/extension.json"
        ]
        recordPackage["license"] = "https://datos.gob.mx/libreusomx"
        recordPackage["publicationPolicy"] = "https://datos.gob.mx/libreusomx"
        recordPackage["publishedDate"] = str(datetime.datetime.utcnow().isoformat()) + 'Z'

        recordPackage["publisher"] = {}
        recordPackage["publisher"]["name"] = "SECRETARÍA DE LA FUNCIÓN PÚBLICA / SECRETARIA DE HACIENDA Y CRÉDITO PÚBLICO"
        # recordPackage["publisher"]["uid"] = "27511"
        recordPackage["publisher"]["uri"] = "http://www.gob.mx/contratacionesabiertas/"

        # recordPackage["packages"] = []
        recordPackage["records"] = []

        record = {}
        record['ocid'] = ocid
        releases = []

        #if cp["conteo"] > 1:
        for release in collection.find({"ocid": ocid}, {"_id": 0}):
            # pprint.pprint(release['date'])
            releases.append(release)

        record["releases"] = releases
        failed = False
        try:
            record["compiledRelease"] = ocdsmerge.merge(releases)
        except:
            print("failed -> ", releases[0]["ocid"])
            failed = True
        # record["versionedRelease"] = ocdsmerge.merge_versioned(releases)

        recordPackage["records"].append(record)

        if not failed:
            if output.lower() == "mongo":
                # insert RecordPackage to mongodb
                RecordPackages = db['RecordPackages']
                # update record if ocid exists in collection
                rp = db.RecordPackages.find_one({"records.compiledRelease.ocid": ocid}, {"_id":1})
                if rp is not None:
                    db.RecordPackages.update(rp, recordPackage)
                else:
                    RecordPackages.insert_one(recordPackage)
            else:
                # write JSON
                file_path = os.path.join(output_dir, ocid + ".json")
                with codecs.open(file_path, 'w', encoding='utf-8') as outfile:
                    json.dump(recordPackage, outfile,ensure_ascii=True,  indent=4)


if __name__ == "__main__":
    main(sys.argv[1:])
