import mod_sdab_libdes
import easygui

def main():
    '''
    main driver script for sdab lib designer; v1.2

    first: get CDR seqs (from fasta via gui) and set user options
    then: loop over list of entries, creating an Antibody object
    finally: formulate dB call, pass results to aa matching code, and format results
    
    '''

    #this _dev points to emblig_homo_sdabs dB;
    print('sdab_libdes, the single-domain antibody library design tool (v1.2)')
    print('freedb.tech dB (v2)')
    print('--> human VH or VL only')
    print('--> IMGT-numbered chains/Ig domains only')
    
    #set user-defined options
    ab_species = 'homo'    #only choice, for now; this will change with other species combos as tables in dB...

    #to get VH or VL, CDR(s) sequences, and lengths of each for matching from fasta file
    ab_fasta_file_path = easygui.fileopenbox()
  #  ab_fasta_file_path = './my_VH_cdr_seqs.fasta'
  #  ab_fasta_file_path = './my_VL_cdr_seqs.fasta'

    #send CDR list to set vars, then fill my_prot_lis) for www CDR tool
    my_prot_list, ab_format, chain_num_scheme, CDR12_annot, CDR3_annot, CDR13_annot = mod_sdab_libdes.prep_seqs(ab_fasta_file_path)



    #create the Antibody object for each CDR entry from the my_prot_list + instance vars
    for i in my_prot_list:

        seq = mod_sdab_libdes.Antibody(i, ab_species, ab_format, chain_num_scheme, CDR12_annot, CDR3_annot, CDR13_annot)

        #split each entry from list (i) into header (id), CDR_match list (which to call dB matching on) and CDR_tool_results_list (CDR seqs)
        header, CDR_match, CDR_tool_results_list = seq.www_CDR_tool()

        #use CDR seq to call to dB with length of users CDRs for matching; returns a list of dicts
        header, CDR_match, CDR_tool_results_list, dB_results_list = seq.call_to_dB(header, CDR_match, CDR_tool_results_list)

        #based on users CDR matching choices (CDR_match), this function reorganizes dB results to do the indiv aa matching
        seq.matching(header, CDR_match, CDR_tool_results_list, dB_results_list)


    table = mod_sdab_libdes.soft_mut_aa_table()
    print(table)


if __name__ == "__main__":
    main()

    '''
    import doctest
    doctest.testmod()
    '''
