# sdab_libdes
Single Domain Antibody Library Designer

sdab_libdes (v1.2)
dB (v2)

DESCRIPTION:
Single Domain Antibody Library Designer is an algorithmic or rule-based script written in Python to design libraries of target-inferfacing CDR mutations of single domain antibody binders, for isolation of an increased affinity mutant by display technology (phage, yeast, etc.).

Efficiently design diversity-containing oligonucleotides for secondary/matured library creation from a human single-domain antibody lead (VL or VH).

Input is the primary sequence(s) of the CDR(s) of a human (VH or VL) lead (per the North, IMGT, or Chothia CDR definition) in the correct text-based, fasta 
file format (see EXAMPLES).
sdab_libdes will search a dB of human single domain antibody CDR sequences (per your CDR definition choice) for matching combined-length CDR entries, VL or VH. 
Same CDR length entries represent sdAbs recognizing a variety of epitopes on a variety of antigens. Individual amino acid matching is performed with a percentage 
homology reported for each position. Given enough matches (~>30), highly-conserved amino acid identities represent residues likely important for domain/interacting 
loop integrity, whereas less well-conserved residues represent locations of antigen interaction, and the focus of mutation for library creation to enhance affinity, 
specificity, etc.

A-priori knowledge of critical antigen interacting CDRs (i.e., via single alanine scanning, etc.), will result in highest tool utility.

CDR definition options available:
VH: CDR-1 + CDR-2 (north, imgt, chothia), CDR-3 (imgt, chothia)
VL: CDR 1-3 (north, imgt, chothia)


dB v2:
human VH or VL only; IMGT-numbered Ig/chains only
--> 56,780 unique VH sequences
--> 28,543 unique VL sequences


	dB v2 amino acid residue range per domain CDR, CDR definition
		most common length (# of dB entries)

		   North	 	   IMGT			  Chothia
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

VL-CDR1		  1 - 24		  1 - 19		  1 - 24
		11 (13,006)		6 (13,055)		11 (13,006)


VL-CDR2		  5 - 14		  2 - 9    		  4 - 13
    		8 (28,110)		3 (28,081)		7 (28,111)
	

VL-CDR3		  3 - 23		  3 - 23		  3 - 23
		9 (12,098)		9 (12,089)		9 (12,098)

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

VH-CDR1		  1 - 23		  1 - 18		  1 - 17
		13 (43,680)		8 (45,233)		 7 (44,118)


VH-CDR2		  3 - 24		  2 - 22		  1 - 20
		10 (37,793)		8 (37,677)		 6 (36,798)


VH-CDR3		    X			  3 - 25		  3 - 21
				    	15 (6,196)	   	11 (6,196)

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



INSTALLATION + USE:

1. With python3 + dependencies (see below) installed, execute main_sdab_libdes.py (with mod_sdab_libdes.py in same folder). 
2. Use pop-up window to navigate to your CDR input file (in fasta file format).
3. In python shell, choose CDR definition(s).
4. Results are printed to standard out/python shell.



INPUT FORMAT + EXAMPLES:

- The order of each user entry should be 6 single-quoted CDR values, comma-separated, and bound by brackets:
['VL-CDR1','VL-CDR2','VL-CDR3','VH-CDR1','VH-CDR2','VH-CDR3']
- VH and VL entries must be contained in separate files and submitted separately.
- All entries within file will be analyzed according to a single CDR definition of your choosing.
- The combination of CDRs to analyze within either the VL or VH file do NOT have to be the same.
- CDR sequences should be UPPERCASE and contained within single quotes.
- For CDRs within VL or VH you do NOT want to analyze, leave blank ('').
- For multiple entries, format of your entries per fasta file format.

--> User input entry(s) determines, 1) which human chain to analyze (VH or VL) and, 2) which CDR's to search dB/match.
--> When prompted, CDR definition choice will apply to ALL entries of submitted file.



2 Input File Examples...

(1) 2 VL entries (The 1st analyzing all 3 VL-CDRs, the 2nd only VL-CDR1+3; both according to the IMGT CDR definition):

>example VL ab0
['ASNIKYSA','ATS','QSFYGSTYWV','','','']
>example VL ab1
['TSNIGRYY','','QSYGTSSGA','','','']


(2) 3 VH entries (The 1st analyzing only VH-CDR1, the 2nd analyzing VH-CDR1+2, the 3rd analyzing all 3 VH-CDRs; all according to the North definition 
for CDR1+2 and the IMGT definition for CDR3):

>example VH ab0
['','','','AASGFTFSSYAMH','','']
>example VH ab1
['','','','ATSFYTFDSYYMT','GISPDGSNTY','']
>example VH ab2
['','','','AASRFTFSSYAMS','IINPSYSNTD','ARDRGSTGFYYYFDY']




Output Example (from Input 1):

sdab_libdes, the single-domain antibody library design tool
--> human VH or VL only
--> IMGT-numbered chains/Ig domains only
----------------------------------------
Reading in entries from fasta file: /Users/guey/Documents/python3/playground/mut_ab_lib_designer/sdab_libdes_v1.2/my_ab_seqs.fasta
----------------------------------------

...
----------------------------------------
Finished reading in 2 entries from fasta file...
----------------------------------------

----------------------------------------
Start of entry: 'example VL ab0'
Matching percentages to all unique CDR combinations from dB of same lengths being calculated...
----------------------------------------
example VL ab0:v1 was 8aa's long;
A:0.26**
S:36.24*
N:41.53*
I:90.74
K:0.26**
Y:3.97**
S:3.7**
A:1.32**
example VL ab0:v2 was 3aa's long;
A:1.32**
T:1.59**
S:5.56**
example VL ab0:v3 was 10aa's long;
Q:61.11
S:62.7
F:5.56**
Y:0.26**
G:6.61**
S:55.82
T:5.03**
Y:7.14**
W:27.51*
V:70.11

The CDR combination(s) of entry: 'example VL ab0' matched with 378 dB records.

dB species searched: homo
Ig chain format: vl
Ig chain numbering scheme: imgt
Light chain CDR 1-3 defintion: imgt

--> ** denotes residues very likely to be directly interacting with your antigen. Hard mutate these to all 19aa; or, at least, to the soft sub-set pattern shown below.
--> * denotes residues likely to be contributing to the direct or supporting interaction with your antigen. Mutate these at least to the soft sub-set pattern shown below, or to all 19 if diversity space allows.
--> Percentages without an * denote residues likely to be playing structural/integriy roles for the interaction with your antigen. Do NOT mutate these.

End of entry.
//


----------------------------------------
Start of entry: 'example VL ab1'
Matching percentages to all unique CDR combinations from dB of same lengths being calculated...
----------------------------------------
example VL ab1:v1 was 8aa's long;
T:6.62**
S:27.53*
N:28.57*
I:89.9
G:29.97*
R:1.05**
Y:5.23**
Y:75.26
example VL ab1:v3 was 9aa's long;
Q:67.6
S:68.29
Y:60.28
G:1.39**
T:12.54**
S:51.57*
S:8.01**
G:15.33**
A:0.35**

The CDR combination(s) of entry: 'example VL ab1' matched with 287 dB records.

dB species searched: homo
Ig chain format: vl
Ig chain numbering scheme: imgt
Light chain CDR 1-3 defintion: imgt

--> ** denotes residues very likely to be directly interacting with your antigen. Hard mutate these to all 19aa; or, at least, to the soft sub-set pattern shown below.
--> * denotes residues likely to be contributing to the direct or supporting interaction with your antigen. Mutate these at least to the soft sub-set pattern shown below, or to all 19 if diversity space allows.
--> Percentages without an * denote residues likely to be playing structural/integriy roles for the interaction with your antigen. Do NOT mutate these.

End of entry.
//
    Soft mutation amino-acid key:

    Non-polar, aliphatic:
        G: Glycine
        A: Alanine
        V: Valine
        L: Leucine
        I: Isoleucine
        M: Methionine

    Non-polar, hydrophobic:
        W: Tryptophan
        F: Phenylalanine
        P: Proline

    Polar:
        S: Serine
        T: Threonine
        N: Asparagine
        Q: Glutamine
    
    Positively charged:
        R: Arginine
        H: Histidine
        L: Lysine

    Negatively charged:
        D: Aspartic Acid
        E: Glutamic Acid







DEPENDENCIES:
python3 (https://www.python.org/downloads/)
easygui (pip3 install easygui)
mysqlconnector (pip3 install mysql-connector-python)



REFERENCE:
-ab source: 
EMBLIG (http://www.abybank.org/emblig/)
-chain/Ig numbering tool: 
ANARCI (https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/anarci/)
-CDR definition tool: 
SCALOP (https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/scalop)



PLANNED FUTURE UPGRADES:
-Primate, rodent, llama Ig domain entries
-Chothia Ig/chain-numbering
-Ability to add v or j region to query for VH and VL
-Ability to add k(appa) or l(ambda) to query for VL
-command line control for results output to directory and filename



COMMENTS:
Log an Issue to leave feedback concerning bugs, enhancements, questions, comments, etc.
