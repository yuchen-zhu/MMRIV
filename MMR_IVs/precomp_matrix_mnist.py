import os
import numpy as np
from util import load_data, ROOT_PATH,_sqdist
from sklearn.decomposition import PCA

def precomp(sname,i,seed=527):
    np.random.seed(seed)
    train, dev, test = load_data(ROOT_PATH+'/data/'+sname+'/main_orig.npz',Torch=False)
    folder = ROOT_PATH+'/tmp/'
    os.makedirs(folder, exist_ok=True)
    if sname in ['mnist_z','mnist_xz']:
        M = int(train.z.shape[0]/400)
        train_K0 = _sqdist(train.z[i*M:(i+1)*M],train.z)
        dev_K0 = _sqdist(dev.z[i*M:(i+1)*M],dev.z)
        np.savez(folder+'{}_K_{}.npz'.format(sname,i),train_K0=train_K0, dev_K0 = dev_K0)
    
    if i < 8 and sname in ['mnist_x','mnist_xz']:
        pca = PCA(n_components=8)
        pca.fit(train.x)
        X = pca.transform(train.x)
        test_X = pca.transform(test.x)
        dev_X = pca.transform(dev.x)

        train_L0 = _sqdist(X[:,[i]],X[:,[i]])
        dev_L0 = _sqdist(dev_X[:,[i]],X[:,[i]])
        test_L0 = _sqdist(test_X[:,[i]],X[:,[i]])
        np.savez(folder+'{}_L_{}.npz'.format(sname,i),train_L0=train_L0, test_L0=test_L0, dev_L0 = dev_L0)

if __name__ == '__main__':
    for ind in range(400):
        for sname in ['mnist_z','mnist_x','mnist_xz']:
            precomp(sname,ind)

    folder = ROOT_PATH+'/mnist_precomp/'
    os.makedirs(folder, exist_ok=True)
    for sname in ['mnist_z','mnist_x','mnist_xz']:
        if sname in ['mnist_z','mnist_xz']:
            train_K0 = []
            dev_K0 = []
            for w_id in range(400):
                res = np.load(ROOT_PATH+'/tmp/{}_K_{}.npz'.format(sname,w_id))
                os.remove(ROOT_PATH+'/tmp/{}_K_{}.npz'.format(sname,w_id))
                train_K0 += [res['train_K0']]
                dev_K0 += [res['dev_K0']]
            train_K0 = np.vstack(train_K0)
            dev_K0 = np.vstack(dev_K0)
            np.save(folder+'{}_train_K0.npy'.format(sname), train_K0)
            np.save(folder+'{}_dev_K0.npy'.format(sname), dev_K0)
            dist = np.sqrt(train_K0)
            a = np.median(dist.flatten())
            np.save(folder+'{}_ak.npy'.format(sname), a)
        
        if sname in ['mnist_x','mnist_xz']:
            train_L0 = []
            test_L0 = []
            for i in range(8):
                L0 = np.load(ROOT_PATH+'/tmp/{}_L_{}.npz'.format(sname,i))
                os.remove(ROOT_PATH + '/tmp/{}_L_{}.npz'.format(sname,i))
                train_L0 += [L0['train_L0']]
                test_L0 += [L0['test_L0']]
            np.savez(folder+'{}_Ls.npz'.format(sname),train_L0=train_L0, test_L0=test_L0)
        

