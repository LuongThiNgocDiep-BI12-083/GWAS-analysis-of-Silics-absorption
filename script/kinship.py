import subprocess
command = "perl ../tasseladmin-tassel-5-standalone-0d3c5f5afd91/run_pipeline.pl -importGuess Input/genotype.hmp.txt -KinshipPlugin -method Centered_IBS -endPlugin -export C:/Users/DiepAnh/Desktop/Intern2023-2024/Rice-GWAS/kinship.txt -exportType SqrMatrix"
try:
    subprocess.run(command, shell=True, check=True)
    print("Run success")
except:
    print("Fail to run")