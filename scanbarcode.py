#!/usr/bin/python

import sys
import json

# barcode = str(sys.argv[2])
# print 'Argument List:', str(sys.argv[1])

def run():
  with open('./index/index.json') as json_file:
    index = json.load(json_file)
    if barcode in index["barcodes"]:
      user = index["names"][index["barcodes"][barcode]]
      # current = index["currentid"]
      currentf = open(".current.txt", "r")
      current = str(currentf.read())

      if user["type"] == "person":
        # if str(index["barcodes"][barcode]) == current:
        if False:
        #   print "Logged out!"
        #   # index["currentid"] = ""
        #   current = ""
            placeholder = "hi"
        else:
          print "Name: ", user["name"]
          print "Please scan equipment to add it to your account."
          print "\nEquipment checked out:"
          for item in user["with"]:
            print "  - ", index["names"][item]["name"]
          # print "\n\n[NOTE] SCAN CARD AGAIN TO LOG OUT (If not checking out/in.)"
          # index["currentid"] = index["barcodes"][barcode]
          current = index["barcodes"][barcode]
      elif (user["type"] == "equipment") & (current != ""):
        current = int(current)
        if index["barcodes"][barcode] in index["names"][current]["with"]:
          print "Checking in equipment '" + user["name"] + "' for account '" + index["names"][current]["name"] + "'."
          index["names"][current]["with"].remove(index["barcodes"][barcode])
          user["with"].remove(current)
          # index["currentid"] = ""
          current = ""
        else:
          print "Checking out equipment '" + user["name"] + "' to account '" + index["names"][current]["name"] + "'."
          index["names"][current]["with"].append(index["barcodes"][barcode])
          user["with"].append(current)
          # index["currentid"] = ""
          current = ""
      elif user["type"] == "equipment":
        print "Please scan your Card first, then scan the equipment."
        print "\nPersons with this equipment:"
        for item in user["with"]:
          print "  - ", index["names"][item]["name"]
    else:
      print "Barcode not defined. Please try again."
      return
    with open('./index/index.json', 'w') as outfile:
      json.dump(index, outfile)
    currentf = open(".current.txt", "w")
    currentf.write(str(current))
    currentf.close()

def getindex():
  with open('./index/index.json') as json_file:
    index = json.load(json_file)
    print "Index:"
    for item in range(len(index["names"])):
      print item," - ", index["names"][item]["name"]

def addp():
  with open('./index/index.json') as json_file:
    index = json.load(json_file)
    id = len(index["names"])
    index["names"].append({"name":name,"type":"person","with":[]})
    index["barcodes"][barcode] = id
    print "\nPerson added! ", name, " can now be used with barcode ", barcode, ".\n\n---"
    with open('./index/index.json', 'w') as outfile:
      json.dump(index, outfile)

def adde():
  with open('./index/index.json') as json_file:
    index = json.load(json_file)
    id = len(index["names"])
    index["names"].append({"name":name,"type":"equipment","with":[]})
    index["barcodes"][barcode] = id
    print "\nEquipment added!", name, "can now be used with barcode", barcode, "\n\n---"
    with open('./index/index.json', 'w') as outfile:
      json.dump(index, outfile)

def addb():
  with open('./index/index.json') as json_file:
    index = json.load(json_file)
    # index["barcodes"].append({"name":name,"type":"equipment","with":[]})
    index["barcodes"][barcode] = int(id)
    print "\nBarcode added!", index["names"][int(id)]["name"], "can now use",barcode , "\n\n---"
    with open('./index/index.json', 'w') as outfile:
      json.dump(index, outfile)


if str(sys.argv[1]) == "scan":
  barcode = str(sys.argv[2])
  run()
elif str(sys.argv[1]) == "index":
  getindex()
elif str(sys.argv[1]) == "addp":
  name = str(sys.argv[2])
  barcode = str(sys.argv[3])
  addp()
elif str(sys.argv[1]) == "adde":
  name = str(sys.argv[2])
  barcode = str(sys.argv[3])
  adde()
elif str(sys.argv[1]) == "addb":
  id = str(sys.argv[2])
  barcode = str(sys.argv[3])
  addb()
  # print "\n[ERROR] Not Implemented Yet.\n"
