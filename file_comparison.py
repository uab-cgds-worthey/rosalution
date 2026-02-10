
rosalution_genes = []

grant_genes = []

with open("rosalution_genes.txt") as file:
  for item in file:
    rosalution_genes.append(item.strip())

with open("grant_genes.txt") as file:
  for item in file:
    grant_genes.extend(item.strip().split(', '))

# print('ROSALUTION GENES!!!!!!!!!!!!!!!!!!!!!!!!!')
# print(rosalution_genes)

# print('GRANT GENES!!!!!!!!!!!!!!!!!!!!!!!!!')
# print(grant_genes)

genes_intersection = set(rosalution_genes) & set(grant_genes)
print(genes_intersection)

print('SORTED GRANT GENES')
print(sorted(grant_genes))