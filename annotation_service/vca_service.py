from flask import Flask, request, Response, send_from_directory, abort
from werkzeug.utils import secure_filename
from os.path import exists
from os import remove
from json import loads
import subprocess

app = Flask(__name__)

vcf_folder = "/mnt/nfs/stored_vcfs/"


@app.route("/files/", methods=["POST"])
def vcf_annotation_bridge():
    try:
        f = request.files["vcf_file"]
    except KeyError:
        return "vcf file not found\n", 400
    return vcf_annotation(f.filename)

def temp_annotate(file_1, file_2):
    command_string = "java -Xmx64g -jar /mnt/nfs/eucancan_vcf_vc/SnpSift/target/SnpSift-4.4.jar dbnsfp -f '1000Gp3_AC,1000Gp3_AF,1000Gp3_AFR_AC,1000Gp3_AFR_AF,1000Gp3_EUR_AC,1000Gp3_EUR_AF,1000Gp3_AMR_AC,1000Gp3_AMR_AF,1000Gp3_EAS_AC,1000Gp3_EAS_AF,1000Gp3_SAS_AC,1000Gp3_SAS_AF,ESP6500_AA_AC,ESP6500_AA_AF,ESP6500_EA_AC,ESP6500_EA_AF,ExAC_AC,ExAC_AF,ExAC_Adj_AC,ExAC_Adj_AF,ExAC_AFR_AC,ExAC_AFR_AF,ExAC_AMR_AC,ExAC_AMR_AF,ExAC_EAS_AC,ExAC_EAS_AF,ExAC_FIN_AC,ExAC_FIN_AF,ExAC_NFE_AC,ExAC_NFE_AF,ExAC_SAS_AC,ExAC_SAS_AF,ExAC_nonTCGA_AC,ExAC_nonTCGA_AF,ExAC_nonTCGA_Adj_AC,ExAC_nonTCGA_Adj_AF,ExAC_nonTCGA_AFR_AC,ExAC_nonTCGA_AFR_AF,ExAC_nonTCGA_AMR_AC,ExAC_nonTCGA_AMR_AF,ExAC_nonTCGA_EAS_AC,ExAC_nonTCGA_EAS_AF,ExAC_nonTCGA_FIN_AC,ExAC_nonTCGA_FIN_AF,ExAC_nonTCGA_NFE_AC,ExAC_nonTCGA_NFE_AF,ExAC_nonTCGA_SAS_AC,ExAC_nonTCGA_SAS_AF,ExAC_nonpsych_AC,ExAC_nonpsych_AF,ExAC_nonpsych_Adj_AC,ExAC_nonpsych_Adj_AF,ExAC_nonpsych_AFR_AC,ExAC_nonpsych_AFR_AF,ExAC_nonpsych_AMR_AC,ExAC_nonpsych_AMR_AF,ExAC_nonpsych_EAS_AC,ExAC_nonpsych_EAS_AF,ExAC_nonpsych_FIN_AC,ExAC_nonpsych_FIN_AF,ExAC_nonpsych_NFE_AC,ExAC_nonpsych_NFE_AF,ExAC_nonpsych_SAS_AC,ExAC_nonpsych_SAS_AF,gnomAD_exomes_AC,gnomAD_exomes_AN,gnomAD_exomes_AF,gnomAD_exomes_AFR_AC,gnomAD_exomes_AFR_AN,gnomAD_exomes_AFR_AF,gnomAD_exomes_AMR_AC,gnomAD_exomes_AMR_AN,gnomAD_exomes_AMR_AF,gnomAD_exomes_ASJ_AC,gnomAD_exomes_ASJ_AN,gnomAD_exomes_ASJ_AF,gnomAD_exomes_EAS_AC,gnomAD_exomes_EAS_AN,gnomAD_exomes_EAS_AF,gnomAD_exomes_FIN_AC,gnomAD_exomes_FIN_AN,gnomAD_exomes_FIN_AF,gnomAD_exomes_NFE_AC,gnomAD_exomes_NFE_AN,gnomAD_exomes_NFE_AF,gnomAD_exomes_SAS_AC,gnomAD_exomes_SAS_AN,gnomAD_exomes_SAS_AF,gnomAD_exomes_OTH_AC,gnomAD_exomes_OTH_AN,gnomAD_exomes_OTH_AF,gnomAD_genomes_AC,gnomAD_genomes_AN,gnomAD_genomes_AF,gnomAD_genomes_AFR_AC,gnomAD_genomes_AFR_AN,gnomAD_genomes_AFR_AF,gnomAD_genomes_AMR_AC,gnomAD_genomes_AMR_AN,gnomAD_genomes_AMR_AF,gnomAD_genomes_ASJ_AC,gnomAD_genomes_ASJ_AN,gnomAD_genomes_ASJ_AF,gnomAD_genomes_EAS_AC,gnomAD_genomes_EAS_AN,gnomAD_genomes_EAS_AF,gnomAD_genomes_FIN_AC,gnomAD_genomes_FIN_AN,gnomAD_genomes_FIN_AF,gnomAD_genomes_NFE_AC,gnomAD_genomes_NFE_AN,gnomAD_genomes_NFE_AF,gnomAD_genomes_OTH_AC,gnomAD_genomes_OTH_AN,gnomAD_genomes_OTH_AF,CADD_phred,CADD_raw,Polyphen2_HDIV_score,Polyphen2_HDIV_pred,Polyphen2_HVAR_score,Polyphen2_HVAR_pred,SIFT_score,SIFT_pred,MutationAssessor_score,MutationAssessor_pred,MutationTaster_score,MutationTaster_pred,FATHMM_score,FATHMM_pred,GERP++_NR,GERP++_RS,LRT_Omega,LRT_score,LRT_pred,MetaLR_score,MetaLR_pred,MetaSVM_score,MetaSVM_pred,Reliability_index,PROVEAN_score,PROVEAN_pred,VEST3_score,M-CAP_score,M-CAP_pred,fathmm-MKL_coding_score,fathmm-MKL_coding_pred,Eigen_coding_or_noncoding,Eigen-raw,Eigen-phred,Eigen-PC-raw,Eigen-PC-phred,integrated_fitCons_score,integrated_confidence_value,GM12878_fitCons_score,GM12878_confidence_value,H1-hESC_fitCons_score,H1-hESC_confidence_value,HUVEC_fitCons_score,HUVEC_confidence_value,GenoCanyon_score,DANN_score,MutPred_score,MutPred_Top5features,REVEL_score,phastCons100way_vertebrate,phastCons20way_mammalian,phyloP100way_vertebrate,phyloP20way_mammalian,SiPhy_29way_pi,SiPhy_29way_logOdds,cds_strand,codonpos,refcodon,codon_degeneracy,Ancestral_allele,Interpro_domain,aapos,Uniprot_aapos_Polyphen2,Uniprot_acc_Polyphen2,Uniprot_id_Polyphen2' -db /mnt/nfs/eucancan_vcf_vc/databases/dbNSFP3.5a_hg19.txt.gz -m -a " + file_1 + " | java -Xmx64g -jar /mnt/nfs/eucancan_vcf_vc/SnpSift/target/SnpSift-4.4.jar annotate -info 'CNT,SOMATIC_STATUS,PRIMARY_SITE,PRIMARY_HISTOLOGY' /mnt/nfs/eucancan_vcf_vc/databases/Cosmic_v84.vcf /dev/stdin -a | java -Xmx64g -jar /mnt/nfs/eucancan_vcf_vc/SnpSift/target/SnpSift-4.4.jar annotate -id -noInfo /mnt/nfs/eucancan_vcf_vc/databases/00-All.vcf.gz /dev/stdin -a | java -Xmx64g -jar /mnt/nfs/eucancan_vcf_vc/SnpSift/target/SnpSift-4.4.jar annotate -id -info 'CLNDISDB,CLNDISDBINCL,CLNDN,CLNSIG,CLNREVSTAT' /mnt/nfs/eucancan_vcf_vc/databases/clinvar.vcf.gz /dev/stdin -a | java -Xmx64g -jar /mnt/nfs/eucancan_vcf_vc/SnpEff/target/SnpEff-4.4.jar GRCh37.p13.RefSeq > " + file_2
    p = subprocess.Popen(['bash', '-c', command_string])
    p.wait()

@app.route("/files/<filename>", methods=["GET","POST","DELETE"])
def vcf_annotation(filename):
    secure_name = secure_filename(filename)
    if request.method == "PUT":
        try:
            f = request.files["new_vcf_file"]
        except KeyError:
            return "vcf file not found\n", 400

        # Empty filename
        if not secure_name:
            return "Malformed or empty file name\n", 422

        # Verify extension
        if not secure_name.lower().endswith(".vcf.gz"):
            return "Unsupported file extension\n", 415

        full_path = "{}{}".format(vcf_folder, secure_name)
        # File already exists
        if exists(full_path):
            return "File already exists\n", 409  # Response(status=409)
        else:
            try:
                f.save(full_path)
            except Exception as e:
                print(e)
                return "Error storing the file\n", 500
            return Response(status=200)
    elif request.method == "DELETE":
        if filename is None or not secure_name:
            return "Malformed or empty file name\n", 422
        full_path = "{}{}".format(vcf_folder, secure_name)
        print("Try to delete {}".format(full_path))
        if exists(full_path):
            remove(full_path)
            return Response(status=200)
        return Response(status=500)
    elif request.method == "GET":
        try:
            return send_from_directory(vcf_folder,
                                       filename=filename, as_attachment=False)
        except FileNotFoundError:
            abort(404)
    """
    elif request.method == "PUT":
        trans_props = loads(request.data)
        print(trans_props)
    """


if __name__ == '__main__':
    app.env="development"
    app.run(debug=False, host="0.0.0.0", port=6000)
