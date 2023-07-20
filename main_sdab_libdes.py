import mod_sdab_libdes
import easygui

def main():
    '''
    main driver for sdab_libdes v1.2

    in general,
    first: read in users CDR seqs (from fasta via gui) and ask/set user options
    then: loop over list of entries, creating an Antibody object for each,
    finally: formulate dB call, pass results to individual aa matching code, and format results, and print to stdout
    
    '''

    #this _dev points to emblig_homo_sdabs dB;
    print('sdab_libdes, the single-domain antibody library design tool')
    print('freedb.tech dB (v2)')
    print('--> human VH or VL only')
    print('--> IMGT-numbered chains/Ig domains only')
    
    #set user-defined options
    ab_species = 'homo'    #only choice, for now; this will change with other species combos as tables in dB...

    #get users fasta file path to file with CDR sequences to analyze, per format stated in README
    ab_fasta_file_path = easygui.fileopenbox()

    #send users list of CDR seqs from fasta file per format instructions (+ with users choices) to list to analyze: 'my_prot_list'
    my_prot_list, ab_format, chain_num_scheme, CDR12_annot, CDR3_annot, CDR13_annot = mod_sdab_libdes.prep_seqs(ab_fasta_file_path)


    #process each users entry from 'my_prot_list' as 'seq' by making an 'Antibody' object + passing users choices as object-instance variables
    for i in my_prot_list:

        seq = mod_sdab_libdes.Antibody(i, ab_species, ab_format, chain_num_scheme, CDR12_annot, CDR3_annot, CDR13_annot)

        #split each entry from list (i) into 1) header (id), 2)CDR_match a list of single char strings (to indicate whether to do dB, indiv
        #aa matching) and, 3)CDR_seqs a list of the literal, string CDR sequences
        header, CDR_match, CDR_seqs = seq.CDR_tool()

        #use lists CDR_match and CDR_seqs and instance vars to call to dB with length of users CDRs for matching; returns a list of dicts
        header, CDR_match, CDR_seqs, dB_results_list = seq.call_to_dB(header, CDR_match, CDR_seqs)

        #based on users CDR matching choices (CDR_match), this function reorganizes dB results to do the indiv aa matching
        seq.matching(header, CDR_match, CDR_seqs, dB_results_list)


    table = mod_sdab_libdes.soft_mut_aa_table()
    print(table)


if __name__ == "__main__":
    main()

    '''
    import doctest
    doctest.testmod()
    '''
