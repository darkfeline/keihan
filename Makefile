PYTHON = python3

srcdir = $(CURDIR)

cluster_targets = $(patsubst $(srcdir)/%-cluster-data.csv,%-cluster-priority.csv,\
	$(wildcard $(srcdir)/*-cluster-data.csv))

.PHONY: all
all: keihan.html mutation-manifest.txt

keihan.html: keihan-template.html cluster-rules.csv
	$(PYTHON) $(srcdir)/render_keihan_page.py $^ >$@

cluster-rules.csv: 2-cluster-priority.csv 3-cluster-priority.csv 4-cluster-priority.csv
	<2-cluster-priority.csv \
	join -t "	" - 3-cluster-priority.csv \
	| join -t "	" - 4-cluster-priority.csv \
	>$@

%-cluster-priority.csv: $(srcdir)/calculate_cluster_priority.py $(srcdir)/%-cluster-data.csv
	$(PYTHON) $(srcdir)/calculate_cluster_priority.py <$(srcdir)/$*-cluster-data.csv >$@

mutation-manifest.txt: $(srcdir)/generate_mutation_manifest.py $(srcdir)/mutation-forms.csv
	$(PYTHON) $(srcdir)/generate_mutation_manifest.py <$(srcdir)/mutation-forms.csv >$@
