import pandas as pd
import os
import glob

fname = "04_기존노선_버스정류장_버퍼300내_인근정류장_결합.csv"
split_by = 950

def spliter(fname, split_by):
    """
    [SPLIT_BY] 기준으로 행을 나눠 csv 생성
    """
    # file_name = '04_기존노선_버스정류장_버퍼300내_인근정류장_결합.csv'
   
    iter_count = 0
    # SPLIT_BY = 950

    df = pd.read_csv('input/' + file_name, encoding='cp949')
    
    for (i, row) in tqdm(df.iterrows(), total=df.shape[0]):
        if i % SPLIT_BY == 0:
            idx_to = i
            idx_from = idx_to - SPLIT_BY
            df[idx_from:idx_to].to_csv('{input_dir}/{file_name}_split_{idx_from}_{idx_to}.csv'
                .format(input_dir='input', file_name=re.sub(".csv", '', file_name), idx_from=idx_from+1, idx_to=idx_to), encoding='utf-8-sig', index=False)
            iter_count += 1

    df[(iter_count-1)*SPLIT_BY:].to_csv('{input_dir}/{file_name}_split_{idx_from}_{idx_to}.csv'
        .format(input_dir='input', file_name=re.sub(".csv", '', file_name), idx_from=(iter_count-1)*SPLIT_BY+1, idx_to=df.shape[0], encoding='utf-8-sig', index=False))

    return df

# spliter(fname, split_by)



def merger(dirname, ext):
    """
    여러개의 csv파일을 읽어 하나의 df로 생성 >> combined.csv로 저장
    """

    directory_name = "output/"
    extension = 'csv'

    os.chdir(directory_name)

    all_fnames = [i for i in glob.glob('*.{}'.format(extension))]

    df = pd.concat([pd.read_csv(f) for f in all_fnames])
    df.to_csv("combined.csv", index=False, encoding='utf-8-sig')

    return df

