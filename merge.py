"""
merge.py:
Genera Records y RecordPackages. Los resultados se pueden escribir a disco o almacenar en MongoDB
"""
import ocdsmerge
import pprint
import json
import datetime
import os
import sys
import getopt
import codecs
from tqdm import tqdm
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

    # MongoDB config
    # client = MongoClient(os.environ.get("MONGODB_TCP_ADDR",'localhost'), os.environ.get("MONGODB_TCP_PORT", 27017))
    client = MongoClient("mongodb://" + os.environ.get("BUDA_FRONT_STORAGE","localhost:27017/buda"))
    buda_db = client.buda # client.EDCA
    edca_db = client.edca
    Releases_collection = edca_db.Releases
    RecordPackages_collection = buda_db['contratacionesabiertas']
    Records_collection = buda_db["Records"]

    output_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "output")

    conteo = Releases_collection.count()
    pbar = tqdm(total = conteo)

    #print ("conteo -> "+ str(conteo))
    for cp in Releases_collection.aggregate([{"$group": {"_id": "$ocid", "conteo": {"$sum": 1 }}}]):
        ocid = cp["_id"]
        # print('Processing -> ', ocid)

        recordPackage = {}
        recordPackage["uri"] = "https://api.datos.gob.mx/v2/"
        recordPackage["version"] = "1.1"
        recordPackage["extensions"] = [
            "https://raw.githubusercontent.com/open-contracting/ocds_location_extension/v1.1.1/extension.json",
            "https://raw.githubusercontent.com/open-contracting/ocds_additionalContactPoints_extension/master/extension.json",
            "https://raw.githubusercontent.com/open-contracting/ocds_budget_breakdown_extension/master/extension.json",
            "https://raw.githubusercontent.com/open-contracting/ocds_contract_suppliers_extension/master/extension.json",
            "https://raw.githubusercontent.com/CompraNet/ocds_releasePublisher_extension/master/extension.json",
            "https://raw.githubusercontent.com/CompraNet/ocds_schemeUrl_extension/master/extension.json"
        ]
        recordPackage["license"] = "https://datos.gob.mx/libreusomx"
        recordPackage["publicationPolicy"] = "https://compranetinfo.funcionpublica.gob.mx/descargas/politica-publicacion-EDCA-MX.pdf"
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
        for release in Releases_collection.find({"ocid": ocid}, {"_id": 0}):
            # pprint.pprint(release['date'])
            releases.append(release)

        record["releases"] = releases
        failed = False
        try:
            record["compiledRelease"] = ocdsmerge.merge(releases, 'release-schema.json')
        except:
            print("failed -> ", releases[0]["ocid"])
            failed = True

        # record["versionedRelease"] = ocdsmerge.merge_versioned(releases)

        recordPackage["records"].append(record)

        if not failed:
            if output.lower() == "mongo":
                # insert RecordPackage to mongodb
                # update record if ocid exists in collection
                """
                rp = RecordPackages_collection.find_one({"records.compiledRelease.ocid": ocid}, {"_id":1})
                if rp is not None:
                    RecordPackages_collection.update(rp, recordPackage)
                    # Records_collection.update()
                else:
                    RecordPackages_collection.insert_one(recordPackage)
                    # Records_collection.insert_one()
                """
                RecordPackages_collection.insert_one(recordPackage)
                Records_collection.insert_one(recordPackage["records"][0])
            else:
                # write JSON
                file_path = os.path.join(output_dir, ocid + ".json")
                with codecs.open(file_path, 'w', encoding='utf-8') as outfile:
                    json.dump(recordPackage, outfile,ensure_ascii=True,  indent=4)
                    
        # update progress bar
        pbar.update(cp.get("conteo", 0))
    pbar.close()

if __name__ == "__main__":
    main(sys.argv[1:])
