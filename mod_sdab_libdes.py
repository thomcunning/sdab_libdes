import mysql.connector


def prep_seqs(ab_fasta_file_path):

###FUTURE ENHANCEMENT: user will be able to choose Ig/chain-numbering scheme; will fill 'dB_table' in dB call; for dB-v2: only imgt

#    chain_num_scheme = input('Select VL or VH Ig chain numbering scheme: {(i)mgt, (c)hothia}')

#    if chain_num_scheme == 'i':
#        chain_num_scheme = 'imgt'

#    elif chain_num_scheme == 'c':
#        chain_num_scheme = 'chothia'

#    else:
#        print('chain numbering scheme choice not recognized. Start again.')


    chain_num_scheme = 'imgt'



    #read-in single domain antibody CDR sequence(s) from fasta file

    fasta_file = open(ab_fasta_file_path,'r')

    print('----------------------------------------')
    print('Reading in entries from fasta file: ' + ab_fasta_file_path)
    print('----------------------------------------')

    my_prot_list = []
    ab_format = ''
    CDR13_annot = ''
    CDR12_annot = ''
    CDR3_annot = ''

    for line in fasta_file:

        if line.startswith('>'):

            header = line.removeprefix('>')
            header = header.strip()
            entry = []
            entry.append(header)

            cdr_line = fasta_file.readline()
            cdr_line = cdr_line.strip()
            cdr_line = cdr_line.removeprefix('[')
            cdr_line = cdr_line.removesuffix(']')
            cdr_line = cdr_line.split(',')  #cdr_line is now a list of CDRs for individual ab entry

            for i in range(len(cdr_line)):
                    
                a = cdr_line[i].removeprefix("'")
                a = a.removesuffix("'")
                a = a.strip()
                a = a.upper()



                #check each CDR for non-amino acid characters; empty '' do not enter this loop...
                for j in a:

                    if j == 'A' or j == 'C' or j =='D' or j =='E' or j =='F' or j =='G' or j =='H' or j =='I' or j =='K' or j =='L' or j =='M' or j =='N' or j =='P' or j =='Q' or j =='R' or j =='S' or j =='T' or j =='V' or j =='W' or j =='Y':

                        continue

                    else:
                        print('****')
                        print('**** Non-amino acid residue \'' + j + '\' found in ' + cdr_line[i] + ' of entry: \'' + header + '\'')
                        print('**** CDR removed from analysis below')
                        print('****')
                        a = ''
                        break

                

                if a.isalpha() and ab_format == '':

                    if i == 0 or i == 1 or i == 2:

                        #VL-CDR1-3 CDR questions
                        #VL-CDR1-3 definition (north:imgt:chothia)
                        ab_format = 'vl'                    
                        CDR13_annot = input('Select which CDR definition to use for human VL-CDR1-3: {(n)orth, (i)mgt, (c)hothia}')

                        if CDR13_annot == 'n' or CDR13_annot == 'N':
                            CDR13_annot = 'north'
                        elif CDR13_annot == 'i' or CDR13_annot == 'I':
                            CDR13_annot = 'imgt'
                        elif CDR13_annot == 'c' or CDR13_annot == 'C':
                            CDR13_annot = 'chothia'
                        else:
                            print('human VL-CDR1-3 definition choice not recognized. Start over.')
                        
                    if i == 3 or i == 4:

                        #VH-1-2 CDR questions
                        #VH-CDR1+2 definition (north, imgt, chothia)
                        ab_format = 'vh'
                        CDR12_annot = input('Select which CDR defintion to use for human VH-CDR1 and VH-CDR2: {(n)orth, (i)mgt, (c)hothia}')
    
                        if CDR12_annot == 'n' or CDR12_annot == 'N':
                            CDR12_annot = 'north'
                        elif CDR12_annot == 'i' or CDR12_annot == 'I':
                            CDR12_annot = 'imgt'
                        elif CDR12_annot == 'c' or CDR12_annot == 'C':
                            CDR12_annot = 'chothia'
                        else:
                            print('human VH-CDR1 and VH-CDR2 defintion choice not recognized. Start over.')
        
                    if i == 5:
    
                        #VH3 CDR questions
                        #VH-CDR3 definition (imgt:chothia)
                        ab_format = 'vh'
                        CDR3_annot = input('Select which CDR definition to use for human VH-CDR3: {(i)mgt, (c)hothia}')

                        if CDR3_annot == 'i' or CDR3_annot == 'I':
                            CDR3_annot = 'imgt'
                        elif CDR3_annot == 'c' or CDR3_annot == 'C':
                            CDR3_annot = 'chothia'
                        else:
                            print('human VH-CDR3 definition choice not recognized. Start over.')


                elif a.isalpha() and ab_format == 'vh' and i == 4:

                        entry.append(a)
                        continue

                elif a.isalpha() and ab_format == 'vh' and i == 5:

                        #VH3 CDR questions
                        #VH-CDR3 definition (imgt:chothia)
                        CDR3_annot = input('Select which CDR definition to use for human VH-CDR3: {(i)mgt, (c)hothia}')

                        if CDR3_annot == 'i':
                            CDR3_annot = 'imgt'
                        elif CDR3_annot == 'c':
                            CDR3_annot = 'chothia'
                        else:
                            print('human VH-CDR3 definition choice not recognized. Start over.')


                entry.append(a)                
#               entry format = [header,'','','','','','']
#               entry format = [header,'l1_seq','l2_seq','l3_seq','h1_seq','h2_seq','h3_seq']



            #logic to NOT add empty entry, where that entry is the first entry of the fasta file (and ab_format has NOT been set yet)
            if entry[1] == '' and entry[2] == '' and entry[3] == '' and entry[4] == '' and entry[5] == '' and entry[6] == '' and ab_format == '':

                print('')
                print('****Error with first entry:' + entry[0])
                print('CDRs all blank...not adding to analysis and moving to next...')
                print('')

            #logic to NOT add empty entries, where that entry is NOT the first entry (i.e., where the ab_format has already been set)
            elif entry[1] == '' and entry[2] == '' and entry[3] == '' and ab_format == 'vl':

                print('')
                print('****Error with VL entry:' + entry[0])
                print('CDRs all blank...not adding to analysis')
                print('')

            elif entry[4] == '' and entry[5] == '' and entry[6] == '' and ab_format == 'vh':

                print('')
                print('****Error with VH entry:' + entry[0])
                print('CDRs all blank...not adding to analysis')
                print('')

            else:
                
                my_prot_list.append(entry)
    #           my_prot_list format = [[header,'','','','','',''],..]



    print('----------------------------------------')
    print('Finished reading in ' + str(len(my_prot_list)) + ' entries from fasta file...')
    print('----------------------------------------')
    print('')
    
    fasta_file.close()
    
    return my_prot_list, ab_format, chain_num_scheme, CDR12_annot, CDR3_annot, CDR13_annot





    
def soft_mut_aa_table():

    soft_mut_aa_table = '''
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

    '''

    return soft_mut_aa_table




class Antibody:

    def __init__(self, i: list, ab_species: str, ab_format: str, chain_num_scheme: str, CDR12_annot: str, CDR3_annot: str, CDR13_annot: str):

        '''
        Antibody object constructor will receive each users entry from 'my_prot_list'
        and be processed (format dB call, receive dB results, perform indiv aa matching) with users-defined options
    
        '''

        #the format of the list 'i' is a list of 7 strings = [header,'l1_seq','l2_seq','l3_seq','h1_seq','h2_seq','h3_seq']
        self.ab_str = i
        
        self.ab_species = ab_species
        self.ab_format = ab_format
        self.chain_num_scheme = chain_num_scheme
        self.CDR12_annot = CDR12_annot
        self.CDR3_annot = CDR3_annot
        self.CDR13_annot = CDR13_annot


    def CDR_tool(self):

        '''
        This function does 3 things:
        1) reads input as the entry CDR (as self.ab_str: a list of strings), takes the first string value as the 'header',  
        2) loops over the next 6 strings, as indicies, and appends those strings (empty or not) into the 6 string list: 'CDR_seqs', then,
        3) fills 'CDR_match' list with 1 (CDR seq as string detected; include in next steps: formulate dB call + do indiv aa matching) or 0 (empty; don't call to dB or do matching), based on if the entry was empty or not.

        FUTURE ENHANCEMENT: have users submit full antibody sequences (not CDRs of antibody in required format)
        would require code to use beautifulsoup, etc. to control browser to fill out web-form + process those results...
        to submit full antibody sequences (as self.ab_str) to an online or internally running SCALOP/SCALOP-like web-form with other required data (ie, users choices)

        '''

        #i = self.ab_str = [header,'l1_seq','l2_seq','l3_seq','h1_seq','h2_seq','h3_seq']

        CDR_match = []
        CDR_seqs = []
        header = self.ab_str[0]
        zero_int = 0
        one_int = 1

        #start at 1, b/c self.ab_str[0] was string 'header'
        for i in range(1,len(self.ab_str)):

            CDR_seqs.append(self.ab_str[i])

            if self.ab_str[i] == '':

                CDR_match.append(zero_int)

            else:

                CDR_match.append(one_int)

        
        #header is string of entry
        #CDR_match is list of single char strings, 0 or 1, to indicate whether to analyze CDR or not
        #CDR_seqs is a list of strings representing the actual CDR sequences
        return header, CDR_match, CDR_seqs        




    def call_to_dB(self, header, CDR_match, CDR_seqs):

        '''
        This function does 2 things:
        1) forms + submits the SQL query based on 1) the users CDR matching choices (ie, 0 or 1 in the input list CDR_match), and 2) the CDR lengths (that comes from the string sequence in input list CDR_seqs)
        2) passes the returned dB results to the next function (macthing) as list of dictionaries

        #FUTURE ENHANCEMENT: make table call dynamic (when more organisms/domain-numbering schemes are added to dB)

        '''
        #set user-defined options
        #self.ab_species            not used here (for db-v2) but will be as part of FUTURE ENHANCEMENT (see below) 
        self.ab_format
        self.chain_num_scheme
        self.CDR12_annot
        self.CDR3_annot
        self.CDR13_annot

        #create the SQL query from 'CDR_match' list and 'CDR_seqs' list using this format...(for dB v2)
        #SELECT DISTINCT vh_imgt_cdr.v1_north, vh_imgt_cdr.v2_north, vh_imgt_cdr.v3_imgt FROM vh_imgt_cdr WHERE CHAR_LENGTH(vh_imgt_cdr.v1_north) = 13 AND CHAR_LENGTH(vh_imgt_cdr.v2_north) = 10 AND CHAR_LENGTH(vh_imgt_cdr.v3_imgt) = 15;

        sql_prefix = 'SELECT DISTINCT '
        sql_table_CDR_title_dynamic=''        
        sql_from = ' FROM '  
        dB_table = self.ab_format + '_' + self.chain_num_scheme + '_cdr'
        sql_where = ' WHERE '
        sql_CDR_charlen_dynamic=''

        sql_final = ''

        print('----------------------------------------')
        print('Start of entry: \'' + header + '\'')

        for i in range(len(CDR_match)): 
            
            if CDR_match[i] == 1:

                if i == 0:    

                    dB_CDR= dB_table + '.v1' + '_' + self.CDR13_annot       #this is for VL-CDR1; for example, 'vl_imgt_cdr.v1_north'

                elif i == 1:

                    dB_CDR= dB_table + '.v2' + '_' + self.CDR13_annot       #this is for VL-CDR2

                elif i == 2:

                    dB_CDR= dB_table + '.v3' + '_' + self.CDR13_annot       #this is for VL-CDR3

                elif i == 3:
                    
                    dB_CDR= dB_table + '.v1' + '_' + self.CDR12_annot       #this is for VH-CDR1
                
                elif i == 4:

                    dB_CDR= dB_table + '.v2' + '_' + self.CDR12_annot       #this is for VH-CDR2                

                elif i == 5:

                    dB_CDR= dB_table + '.v3' + '_' + self.CDR3_annot        #this is for VH-CDR3


                sql_table_CDR_title_dynamic = sql_table_CDR_title_dynamic + dB_CDR + ', '
                sql_CDR_charlen_dynamic = sql_CDR_charlen_dynamic + 'CHAR_LENGTH('+ dB_CDR + ') = ' + str(len(CDR_seqs[i])) + ' AND '


        #make final edits to substrings of final sql query string
        sql_table_CDR_title_dynamic = sql_table_CDR_title_dynamic.removesuffix(', ')
        sql_CDR_charlen_dynamic = sql_CDR_charlen_dynamic.removesuffix(' AND ')
        sql_CDR_charlen_dynamic = sql_CDR_charlen_dynamic + ';'

        #final SQL query for db v2
        sql_final = sql_prefix + sql_table_CDR_title_dynamic + sql_from + dB_table + sql_where + sql_CDR_charlen_dynamic         




        #open dB connnection over network...
        
## local
#        config = {'user': 'root',
#          'password': 'root',
#          'host': '127.0.0.1',
#          'port': 8889,
#          'database': 'emblig_homo_sdabs', 
#          'raise_on_warnings': True
#        }


## pro.freedb.tech
        config = {'user': 'thomas',
        'password': 'GKR&5TH3pg97wu@',
        'host': 'pro.freedb.tech',         
        'port': 3306,

        #FUTURE ENHANCEMENT: dynanmic based on user-defined species they want to search, as set in 'self.ab_species' var in main driver (ie, NOT in db v2)
        'database': 'EmbligHomoSdabs',      
        'raise_on_warnings': True
        }

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(sql_final)

        #dB_results_list is formated as a list of dictionaries; where the dicts are a single CDR title as key (ie, 'v1_north') : single string of sequence as value ('LEDCVNWPTAM')
        dB_results_list = cursor.fetchall()
        
        cnx.close()

        return header, CDR_match, CDR_seqs, dB_results_list



    def matching(self, header, CDR_match, CDR_seqs, dB_results_list):

        '''
        If there were results returned from dB call...
            ...based on the users CDR matching preferences (in list CDR_match), this function: (if set to 1, set var to unique dynamic string ('CDR_CDRdef'))
            1) reorganizes the given, individual CDRs matches returned from the dB_results ('dB_results_list') to a temporary list ('reorg_CDR_result'),
            2) individual amino acid matching between users CDR sequence (from 'CDR_seqs') and the re-organized dB results (in 'reorg_CDR_result'),
            3) formats the stdout for display (by calling 'format_for_display' function)
        '''


        #make a list of strings from the dB results if the individual CDR (in 'CDR_CDRdef') match


        #set user-defined options
        self.ab_species
        self.ab_format
        self.chain_num_scheme
        self.CDR12_annot
        self.CDR3_annot
        self.CDR13_annot

        #IF there are NO dB records returned for the entry...

        if dB_results_list == []:
        
            print('There are 0 dB records for the CDR length combinations of entry: \'' + header + '\' per the \'' + self.chain_num_scheme + '\' chain-numbering scheme, with the following chosen CDR definition(s).')

            if self.CDR12_annot != '':
        
                print('Heavy chain CDR 1+2 defintion: ' + self.CDR12_annot)

            if self.CDR3_annot != '':
            
                print('Heavy chain CDR 3 defintion: ' + self.CDR3_annot)

            if self.CDR13_annot != '':

                print('Light chain CDR 1-3 defintion: ' + self.CDR13_annot)


        #IF there are dB records returned for the entry...

        else:

            print('Matching percentages to all unique CDR combinations from dB of same lengths being calculated...')
            print('----------------------------------------')

            for i in range(len(CDR_match)):

                if CDR_match[i] == 1:
                
                    if i == 0:
                        # for VL-CDR1; for example, 'v1_north'
                        CDR_CDRdef = 'v1' + '_' + self.CDR13_annot
                        CDR_num = 0
                    
                    elif i == 1:
                        # for VL-CDR2
                        CDR_CDRdef = 'v2' + '_' + self.CDR13_annot
                        CDR_num = 1
                    
                    elif i == 2:
                        # for VL-CDR3
                        CDR_CDRdef = 'v3' + '_' + self.CDR13_annot
                        CDR_num = 2
                    
                    elif i == 3:
                        # for VH-CDR1; for example, 'v1_imgt'
                        CDR_CDRdef = 'v1' + '_' + self.CDR12_annot
                        CDR_num = 3
                    
                    elif i == 4:
                        # for VH-CDR2
                        CDR_CDRdef = 'v2' + '_' + self.CDR12_annot
                        CDR_num = 4
                    
                    elif i == 5:
                        # for VH-CDR3;; for example, 'v3_imgt'
                        CDR_CDRdef = 'v3' + '_' + self.CDR3_annot
                        CDR_num = 5


                    #initiate list for re-organized dB results for that CDR here
                    reorg_CDR_result = []
    
                    #iterate over each dict entry in the dB returned, un-organized list
                    for j in dB_results_list:

                        dB_results_keys = j.keys()

                        #iterate over the keys for that individual dict entry
                        for k in dB_results_keys:

                            #if key from individual dict entry matches with that of users preference, fill the 'reorg_CDR_result' list with the sequence strings for that CDR
                            if k == CDR_CDRdef:
                                
                                reorg_CDR_result.append(j[k])    #or, dB_results_list[j;must be index][k:must be string]
                    
                    #fill 'my_CDR_str' with CDR amino acid string sequence and initiate list to hold matching percentages per amino acid for entire CDR ('ALL_aaID_matchFLT')
                    my_CDR_str = CDR_seqs[CDR_num]
                    ALL_aaID_matchFLT = []

                    #iterate over 'my_CDR_str', fill a list ('INDIV_aaID_matchFLT') with each amino acid residue's alphabetical uppercase character as a string (thats the 'INDIV_aaID' part),
                    #then ask if it matches with same index position for each re-organzed dB match for that CDR, if so increment 'match_increment' var
                    #finally, do some simple math with positive matches (in match_incremet; as numerator) and number of total CDR matches for that CDR (in reorg_CDR_result; as denominator) and assign to 'match_float'
                    #add 'match_float' to its corresponding single letter amino acid string, assign to list 'INDIV_aaID_matchFLT'; a 2 value list of a string and a float
                    #finally, add 'INDIV_aaID_matchFLT' list to the list 'ALL_aaID_matchFLT' that holds all amino acids and their matching %'s, and pass that to definition: 'self.format_for_display' for added info to stdout. 

                    for m in range(len(my_CDR_str)):
                    
                        match_increment = 0
                        INDIV_aaID_matchFLT = []
                        INDIV_aaID_matchFLT.append(my_CDR_str[m])
            
                        for n in reorg_CDR_result:    

                            if my_CDR_str[m] == n[m]:
    
                                match_increment +=1

                        match_float = (match_increment / len(reorg_CDR_result))*100

                        #individual amino acid as string + corresponding matching percentage as float; ['Q',72.1]
                        INDIV_aaID_matchFLT.append(round(match_float,2))

                        #for indiv CDR, a list of 2 value lists for ALL individual amino acids as strings + corresponding matching percentage as floats: [['V',35.8],['Q',72.1],...]
                        ALL_aaID_matchFLT.append(INDIV_aaID_matchFLT)
                    

                    #Top line message, printed per analyzed CDR
                    CDR_label = CDR_CDRdef.split('_')   # becomes a 2 value list 
                    print(header + ':' + CDR_label[0] + ' was ' + str(len(my_CDR_str)) + 'aa\'s long;')

                    #Give added info for the individual aa matching %'s by passing 'ALL_aaID_matchFLT' list to def: format_for_display
                    self.format_for_display(ALL_aaID_matchFLT)
                
                print('',end='')


            #final results lines here
            print('')
            print('The CDR combination(s) of entry: \'' + header + '\' matched with ' + str(len(reorg_CDR_result)) + ' dB records.')
            print('')

            print('dB species searched: ' + self.ab_species)
            print('Ig chain format: ' + self.ab_format)
            print('Ig chain numbering scheme: ' + self.chain_num_scheme)

            if self.CDR12_annot != '':
        
                print('Heavy chain CDR 1+2 defintion: ' + self.CDR12_annot)

            if self.CDR3_annot != '':
            
                print('Heavy chain CDR 3 defintion: ' + self.CDR3_annot)

            if self.CDR13_annot != '':

                print('Light chain CDR 1-3 defintion: ' + self.CDR13_annot)

            print('')
            print('--> ** denotes residues very likely to be directly interacting with your antigen. Hard mutate these to all 19aa; or, at least, to the soft sub-set pattern shown below.')
            print('--> * denotes residues likely to be contributing to the direct or supporting interaction with your antigen. Mutate these at least to the soft sub-set pattern shown below, or to all 19 if diversity space allows.')
            print('--> Percentages without an * denote residues likely to be playing structural/integriy roles for the interaction with your antigen. Do NOT mutate these.')
            print('')
            print('End of entry.')
            print('//')
            print('')
            print('')


    def format_for_display(self, ALL_aaID_matchFLT):


        for i in ALL_aaID_matchFLT:

            if i[1] <= 25.0:
                print(i[0] + ':' + str(i[1]) + '**')
            elif i[1] <=55.0:
                print(i[0] + ':' + str(i[1]) + '*')
            else:
                print(i[0] + ':' + str(i[1]))        
