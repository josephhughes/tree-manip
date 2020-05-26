#!/usr/bin/env python3

# python Prune.py --tree ~/Documents/Coronavirus/cog20200508/cog_global_2020-05-08_tree.newick --keyword Scotland --out Scottish_ncov.tre

import argparse
from ete3 import Tree
import sys
import re

# Loads a tree structure from a newick file
parser = argparse.ArgumentParser(description="Prune a tree keeping tip labels that contain a particular string", add_help=False)
parser.add_argument("--tree", help="The newick tree file.\n")
parser.add_argument("--keyword", help="Keyword to look for in the tip label.\n")
parser.add_argument("--out", help="The output pruned tree in newick format.\n")
parser.add_argument("-h","--help", action="store_true")
args = parser.parse_args()

def custom_help():
    print("Required Arguments!!\n\t--tree [file.newick]\n")
    print("\t--keyword [text]\n")
    print("\t--out [output.newick]\n")

if len(sys.argv) < 3 or args.help:
  print(custom_help())
  exit(1)

with open(args.tree, 'r') as file:
    data = file.read().replace('\n', '')

data=data.replace("[&R] ","")
t = Tree(data,format=1)

keep=0;
keeping=[]
for leaf in t:
  # Do some analysis on node
  #print(node.name)
  if args.keyword in leaf.name:
    print(leaf.name)
    keep+=1
    keeping.append(leaf.name)
# the following doesn't correctly preserve branch lengths    
#   else:
#     leaf.delete()
print("Keeping ",keep," sequences")
t.prune(keeping,preserve_branch_length=True)

t.write(format=1, outfile=args.out)