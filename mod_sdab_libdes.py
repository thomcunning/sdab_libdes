import mysql.connector


def prep_seqs(ab_fasta_file_path):

    #variable region/chain numbering scheme; will point to specific dB_table to get CDRs from (imgt, or chothia when avail)

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

    def __init__(self, i: list, ab_species: str, ab_format: str, chain_num_scheme: str, CDR12_annot: str, CDR3_annot: str, CDR13_annot: str, extra_info="N/A", other_var=None):

        '''
        Antibody object constructor.
        User's CDR sequence(s) from file looped over and processed with users-defined options
    
        '''

        #i = self.ab_str = [header,'l1_seq','l2_seq','l3_seq','h1_seq','h2_seq','h3_seq']
        self.ab_str = i
        
        self.ab_species = ab_species
        self.ab_format = ab_format
        self.chain_num_scheme = chain_num_scheme
        self.CDR12_annot = CDR12_annot
        self.CDR3_annot = CDR3_annot
        self.CDR13_annot = CDR13_annot
        
        self.extra_info = extra_info
        self.other_var = other_var



    def www_CDR_tool(self):

        '''
        This function does 3 things:
        1) reads in an entry CDR (as self.ab_str), takes the first value as the 'header',  
        2) loops over its indicies 1 to 6 and fills CDR seqs (empty or not) into 'CDR_tool_results_list', also
        3) fills 'CDR_match' list with 1(not empty; make apart of dB call + do matching) or 0(empty; dont call to dB or do matching), based on if the entry was empty or not.

        '''
        #or, code to submit self.ab_str to online/internal SCALOP form with required data (ie, users choices)

        #i = self.ab_str = [header,'l1_seq','l2_seq','l3_seq','h1_seq','h2_seq','h3_seq']

        CDR_match = []
        CDR_tool_results_list = []
        header = self.ab_str[0]
        zero_int = 0
        one_int = 1

        for i in range(1,len(self.ab_str)):

            CDR_tool_results_list.append(self.ab_str[i])

            if self.ab_str[i] == '':

                CDR_match.append(zero_int)

            else:

                CDR_match.append(one_int)

        

        return header, CDR_match, CDR_tool_results_list        




    def call_to_dB(self, header, CDR_match, CDR_tool_results_list):


        '''
        This function principally does 2 things:
        1) forms the SQL command based on the users CDR matching choices + CDR lengths and submits to dB
        2) passes results to next function as list of dicts
        #returned dB results = a list of dictionaries with single CDR titles as keys ('v1_north'): string of sequences as values('LEDCVNWPTAM')
        '''


        #set user-defined options
        self.ab_species
        self.ab_format
        self.chain_num_scheme
        self.CDR12_annot
        self.CDR3_annot
        self.CDR13_annot

        #create the SQL command from 'CDR_match' and 'CDR_tool_results_list' using this format, for example...
        #dB (v2)
        #SELECT DISTINCT vh_imgt_cdr.v1_north, vh_imgt_cdr.v2_north, vh_imgt_cdr.v3_imgt FROM vh_imgt_cdr WHERE CHAR_LENGTH(vh_imgt_cdr.v1_north) = 13 AND CHAR_LENGTH(vh_imgt_cdr.v2_north) = 10 AND CHAR_LENGTH(vh_imgt_cdr.v3_imgt) = 15;

        #For now, just match to dB with desired CDRs to match + length (ab format)

        dB_prefix = 'SELECT DISTINCT '
        dB_dynamic1=''        
        dB_midfix = ' FROM '  
        dB_table = self.ab_format + '_' + self.chain_num_scheme + '_cdr'
        dB_postfix = ' WHERE '
        dB_dynamic2=''
        
        dB_incrementer = 0

        print('----------------------------------------')
        print('Start of entry: \'' + header + '\'')
        #print('Calling to dB...')

        for i in range(len(CDR_match)):        #the designer CDRs the user wants to do matching with; for dB_dyanmic1
            
            if CDR_match[i] == 1:

                dB_incrementer +=1

                if i == 0:    

                    dB_CDR= dB_table + '.v1' + '_' + self.CDR13_annot       #this is the VL CDR1-3 var

                elif i == 1:

                    dB_CDR= dB_table + '.v2' + '_' + self.CDR13_annot       #this is the VL CDR1-3 var

                elif i == 2:

                    dB_CDR= dB_table + '.v3' + '_' + self.CDR13_annot       #this is the VL CDR1-3 var

                elif i == 3:
                    
                    dB_CDR= dB_table + '.v1' + '_' + self.CDR12_annot       #self.CDR12_annot is the VH chain cdr1+2 var
                
                elif i == 4:

                    dB_CDR= dB_table + '.v2' + '_' + self.CDR12_annot       #self.CDR12_annot is the VH chain cdr1+2 var                

                elif i == 5:

                    dB_CDR= dB_table + '.v3' + '_' + self.CDR3_annot       #self.CDR3_annot is the VH chain cdr3 var


                dB_dynamic1 = dB_dynamic1 + dB_CDR + ', '
                dB_dynamic2 = dB_dynamic2 + 'CHAR_LENGTH('+ dB_CDR + ') = ' + str(len(CDR_tool_results_list[i])) + ' AND '


        if dB_incrementer !=0:
            dB_dynamic1 = dB_dynamic1.removesuffix(', ')
            dB_dynamic2 = dB_dynamic2.removesuffix(' AND ')
            dB_dynamic2 = dB_dynamic2 + ';'


    #   final SQL statement
        dB_dynamic1 = dB_prefix + dB_dynamic1 + dB_midfix + dB_table + dB_postfix + dB_dynamic2         ##v2
 
    ##    print(dB_dynamic1)

        #open dB connnection over network...

## local
#        config = {'user': 'root',
#          'password': 'root',
#          'host': '127.0.0.1',
#          'port': 8889,
#          'database': 'emblig_homo_sdabs',      #this will change based on self.ab_species variable in driver script; 'emblig_' + self.ab_species + '_sdabs'
#          'raise_on_warnings': True
#        }


## pro.freedb.tech - (v2)
        config = {'user': 'thomas',
        'password': 't7JM@nNM?*@KzK6',
        'host': 'pro.freedb.tech',         
        'port': 3306,
        'database': 'EmbligHomoSdabs',      #this will change based on self.ab_species variable in driver script; 'emblig_' + self.ab_species + '_sdabs'
        'raise_on_warnings': True
        }


        cnx = mysql.connector.connect(**config)

        cursor = cnx.cursor(dictionary=True)

        cursor.execute(dB_dynamic1)

        dB_results_list = cursor.fetchall()
        
        #results is a list of dictionaries with single CDR titles as keys ('v1_north'): string of sequences as values('LEDCVNWPTAM')
        #print(dB_results_list)

        cnx.close()

        return header, CDR_match, CDR_tool_results_list, dB_results_list




    def matching(self, header, CDR_match, CDR_tool_results_list, dB_results_list):

        '''
        Based on the users CDR matching preferences (in self.CDR_match), this function:
        1) reorganizes the given CDR's matches returned from the dB_results (in 'dB_results_list') to a temporary list ('filler_list'),
        2) does the individual amino acid matching between users CDR sequence (from 'CDR_tool_results_list') and the re-organized dB results (in 'filler_list'),
        3) formats the stdout for display (by calling 'format_for_display' function)
        '''

        #iterate over users preferences (from 'CDR_match'), if set to 1, set some var to unique dynamic string ('CDR_var')
        #make a list of strings from the dB results if the individual CDR (in 'CDR_var') match


        #set user-defined options
        self.ab_species
        self.ab_format
        self.chain_num_scheme
        self.CDR12_annot
        self.CDR3_annot
        self.CDR13_annot



        #if there are dB records for the entry...

        if dB_results_list == []:
        
            print('There are 0 dB records for the CDR length combinations of entry: \'' + header + '\' per the \'' + self.chain_num_scheme + '\' chain-numbering scheme, with the following chosen CDR definition(s).')

            if self.CDR12_annot != '':
        
                print('Heavy chain CDR 1+2 defintion: ' + self.CDR12_annot)

            if self.CDR3_annot != '':
            
                print('Heavy chain CDR 3 defintion: ' + self.CDR3_annot)

            if self.CDR13_annot != '':

                print('Light chain CDR 1-3 defintion: ' + self.CDR13_annot)


        else:

            print('Matching percentages to all unique CDR combinations from dB of same lengths being calculated...')
            print('----------------------------------------')

            for i in range(len(CDR_match)):

                if CDR_match[i] == 1:
                
                    if i == 0:
                        # VL-CDR1
                       # CDR_var = 'v1_north'
                        CDR_var = 'v1' + '_' + self.CDR13_annot
                        CDR_num = 0
                    
                    elif i == 1:
                        # VL-CDR2
                       # CDR_var = 'v2_north'
                        CDR_var = 'v2' + '_' + self.CDR13_annot
                        CDR_num = 1
                    
                    elif i == 2:
                        # VL-CDR3
                       # CDR_var = 'v3_north'
                        CDR_var = 'v3' + '_' + self.CDR13_annot
                        CDR_num = 2
                    
                    elif i == 3:
                        # VH-CDR1
                       # CDR_var = 'v1_north'
                        CDR_var = 'v1' + '_' + self.CDR12_annot
                        CDR_num = 3
                    
                    elif i == 4:
                        # VH-CDR2
                       # CDR_var = 'v2_north'
                        CDR_var = 'v2' + '_' + self.CDR12_annot
                        CDR_num = 4
                    
                    elif i == 5:
                        # VH-CDR3
                      #  CDR_var = 'v3_imgt'
                        CDR_var = 'v3' + '_' + self.CDR3_annot
                        CDR_num = 5


                    #initiate list for re-organized dB results for that CDR here
                    filler_list = []
    
                    #iterate over each dict entry in the dB returned, un-organized list
                    for j in dB_results_list:

                        results_keys_var = j.keys()

                        #iterate over the keys for that individual dict entry
                        for k in results_keys_var:

                            #if key from individual dict entry matches with that of users preference, fill the 'filler_list' seqs for that CDR
                            if k == CDR_var:
                                
                                filler_list.append(j[k])    #or, dB_results_list[j;must be index][k:must be string]
                    
                    #fill 'my_CDR_str' with CDR aa sequence
                    my_CDR_str = CDR_tool_results_list[CDR_num]
                    matching_list_CDR = []

                    #iterate over 'my_CDR_str', fill a temp list ('storage_list') with each amino acid residue's alphabetical uppercase character,
                    #then ask if it matches with same index position for each re-organzed dB match for that CDR,
                    #do some simple math with incremeter and fill storage list with 2nd value; the final matching %
                    for m in range(len(my_CDR_str)):
                    
                        incre_match = 0
                        storage_list = []
                        storage_list.append(my_CDR_str[m])
            
                        for n in filler_list:    

                            if my_CDR_str[m] == n[m]:
    
                                incre_match +=1

                        position_match_flt = (incre_match / len(filler_list))*100

                        storage_list.append(round(position_match_flt,2))

                        matching_list_CDR.append(storage_list)
                    

                    #Top line message, printed per analyzed CDR
                    CDR_label = CDR_var.split('_')   # becomes a 2 value list 
                    print(header + ':' + CDR_label[0] + ' was ' + str(len(my_CDR_str)) + 'aa\'s long;')

                    #The individual aa matching %'s
                    self.format_for_display(matching_list_CDR)
                
                print('',end='')


            #final results lines here
            print('')
            print('The CDR combination(s) of entry: \'' + header + '\' matched with ' + str(len(filler_list)) + ' dB records.')
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
            print('--> ** denotes residues very likely to be directly interacting with your antigen. Hard mutate these to all 19aa; or, at least, to the soft sub-set pattern per key below.')
            print('--> * denotes residues likely to be contributing to the direct or supporting interaction with your antigen. Mutate these at least to the soft sub-set pattern shown per key below, or to all 19, if diversity space allows.')
            print('--> Percentages without an * denote residues likely to be playing structural/integriy roles for the interaction with your antigen. Do NOT mutate these.')
            print('')
            print('End of entry.')
            print('//')
            print('')
            print('')


    def format_for_display(self, matching_list_CDR):


        for i in matching_list_CDR:

            if i[1] <= 25.0:
                print(i[0] + ':' + str(i[1]) + '**')
            elif i[1] <=55.0:
                print(i[0] + ':' + str(i[1]) + '*')
            else:
                print(i[0] + ':' + str(i[1]))        
