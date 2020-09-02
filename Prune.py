#!/usr/bin/env python3

# python Prune.py --tree ~/Documents/Coronavirus/cog20200508/cog_global_2020-05-08_tree.newick --keyword Scotland --out Scottish_ncov.tre

import argparse
from ete3 import Tree
import sys
import re

# Loads a tree structure from a newick file
parser = argparse.ArgumentParser(description="Prune a tree keeping tip labels that contain a particular string", add_help=False)
parser.add_argument("--tree", help="The newick tree file.\n")
parser.add_argument("--keyword", help="Keyword to look for in the tip label, can be multiple words comma separated England,Scotland.\n")
parser.add_argument("--remove", help="List of tips to remove.\n")
parser.add_argument("--keep", help="List of tips to keep and remove the rest.\n")
parser.add_argument("--out", help="The output pruned tree in newick format.\n")
parser.add_argument("-h","--help", action="store_true")
args = parser.parse_args()

def custom_help():
    print("Required Arguments!!\n\t--tree [file.newick]\n")
    print("\t--keyword [text]\n")
    print("\t--remove [file.txt]\n")
    print("\t--keep [file.txt]\n")
    print("\t--out [output.newick]\n")

if len(sys.argv) < 3 or args.help:
  print(custom_help())
  exit(1)

with open(args.tree, 'r') as file:
    data = file.read().replace('\n', '')

data=data.replace("[&R] ","")
data=data.replace("'","")
t = Tree(data,format=1)



keep=0;
keeping=[]

if (args.keyword):
  keywords = args.keyword.split(",")  
  for leaf in t:
    # Do some analysis on node
    #print(node.name)
  
    #if args.keyword in leaf.name:
    if any(word in leaf.name for word in keywords):
      print(leaf.name)
      keep+=1
      keeping.append(leaf.name)
   # the following doesn't correctly preserve branch lengths    
   #   else:
   #     leaf.delete()

remove=[]  
if (args.remove):
  with open(args.remove, 'r') as file:
    for aRow in file:
      vals=aRow.strip().split('\t')
      print(vals[0])
      remove.append(vals[0])
  file.close()
  print("*********")
  print(remove)
  for leaf in t:
    if leaf.name not in remove:
      print(leaf.name)
      keep+=1
      keeping.append(leaf.name)
    else:
      print("Removing "+leaf.name)

keeplist=[]
if (args.keep):
  with open(args.keep, 'r') as file:
    for aRow in file:
      vals=aRow.strip().split('\t')
      print(vals[0])
      keeplist.append(vals[0])
  file.close()
  print("*********\nIds to keep\nChecking if they are in the tree\n*********")
  print(keeplist)
  for leaf in t:
    if leaf.name in keeplist:
      print(leaf.name)
      keep+=1
      keeping.append(leaf.name)
    else:
      print("Removing "+leaf.name)
     
   
print("Keeping ",keep," sequences")
t.prune(keeping,preserve_branch_length=True)

t.write(format=1, outfile=args.out)