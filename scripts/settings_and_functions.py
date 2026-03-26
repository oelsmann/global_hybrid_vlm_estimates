import copy
import warnings

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas
import matplotlib as mpl
import matplotlib
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
import seaborn as sns
import tifffile
import xarray as xr

from cartopy.io import shapereader
from fuzzywuzzy import fuzz, process
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from PIL import Image
from rasterio.transform import xy
from scipy.optimize import minimize
from scipy.spatial import cKDTree
from scipy.stats import gaussian_kde, johnsonsu
from sealeveltools.sl_class import *
from sklearn.exceptions import ConvergenceWarning
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, RBF, WhiteKernel
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings(
    "ignore",
    message=".*ChainedAssignmentError.*",
    category=FutureWarning,
)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)



settings = {}

settings['data_in'] = './input_data/'
settings['plot_ext'] = '../figures/SI_Figures/'
settings['plot_main'] = '../figures/SI_Main/'
settings['output_data']= './data/'

settings['Version'] = '6'

settings['Version_info'] = {'2':'InSAR Cities',
                            '3':'v2 + InSAR China',
                            '3.01':'v3 + InSAR USA',
                            '3.02':'v3 + InSAR EU',
                            '3.03':'v3 + InSAR USA + EU + Deltas',
                            '5':'v3 + InSAR USA + EU + Deltas + GPS at 50k cities',
                            '6':'v5 + GPS at global islands'}

settings['Version_info_2'] = {'VLM_InSAR<v>': 'contains only data as sepcified in Version_info',
                              'VLM_map_InSAR<v>': 'contains data Version_info + OE25 ',
                              'VLM_map_InSAR<v>_GIA': 'contains data Version_info + OE25 + GIA'}

# Cross-validation errors
settings['datatypes_info'] = { '0':['InSAR Cities',1.72],
                               '1':['InSAR NZ',1.6],
                               '2':['InSAR China',1.5],
                               '3':['InSAR USA',1.43],
                               '4':['InSAR EU',1.19],
                               '5':['GNSS',0],
                               '6':['InSAR Deltas',1.2],
                               '7':['Mississippi',0], # RSET-based
                               '8':['OE24',0],
                               '9':['GIA',0]}

main_fontsize = 13
labelsize=12
plt.rc('axes', unicode_minus=False)
max_width =12
plt.rcParams.update({'font.sans-serif':'Helvetica'})
plt.rcParams['figure.dpi'] = 200 
aspect= 1.15

# variables
cmap_err = sns.diverging_palette(220, 20, as_cmap=True)




def red_blue_no_white():
    N = 256
    # take bottom part of Blues (dark blue)
    blues = cmap_err(np.linspace(0.6, 1, N//2))
    # take top part of Reds (strong red)
    reds  = cmap_err(np.linspace(0,0.4, N//2))
    # stack: red → blue (no white in center)
    colors = np.vstack((reds, blues))
    return LinearSegmentedColormap.from_list("red_blue_nowhite", colors)

cmap_no_white = LinearSegmentedColormap.from_list(
    "custom_rb",
    [cmap_err(0.95),'#9990AA', cmap_err(0.05)][::-1],
    N=256
)

cmap_no_white = LinearSegmentedColormap.from_list(
    "custom_rb",
    [cmap_err(0.95),"#B14E8A", cmap_err(0.05)][::-1],
    N=256
)

cmap_val=cmap_no_white



def darken(color, factor=0.45):
    r, g, b, a = mpl.colors.to_rgba(color)
    return (r*factor, g*factor, b*factor, a)

base = copy.deepcopy(cmap_err)

# anchors from original cmap positive half
c_white = base(0.5)      # center (white-ish)
c_red   = base(1.0)      # original max red
c_dark  = '#fa07ad' #darken(c_red, factor=0.6)  # much darker red



c_white = base(0.5)      # center (white-ish)
c_red   = '#fac507'     # original max red
c_dark  = base(1.0) #darken(c_red, factor=0.6)  # much darker red

# anchors from original cmap positive half
c_white = base(0.5)      # center (white-ish)
c_red   = base(1.0)      # original max red
c_dark  = darken(c_red, factor=0.6)  # much darker red



pos_anchors = [c_white, c_red, c_dark]
pos_cmap = mpl.colors.LinearSegmentedColormap.from_list("pos_darkred", pos_anchors)

# rebuild full cmap: keep first half, replace second half
n = 256
first_half = base(np.linspace(0.0, 0.5, n//2))
second_half = pos_cmap(np.linspace(0, 1, n//2))
cmap_mod = mpl.colors.ListedColormap(np.vstack([first_half, second_half]), name="div_darkred_pos")














def delete_regions_manual(data_in,list_of_boxes=[]):
    # lon,lat,lon,lat
    
    data_in=copy.deepcopy(data_in)
    
    boxes_delete = list_of_boxes

    lat=data_in.lat.values
    lon=data_in.lon.values
    selector = [True]*len(lat)
    for box in boxes_delete:
        selector=selector & ~((lat >= box[2]) & (lat <= box[3]) & (lon >= box[0]) & (lon <= box[1]))
    data_in=data_in.sel({'x':selector}) 
    return data_in
    
def v_lat(lat):
    delta_v = -2e-4*lat**2 + 0.04*lat - 0.85
    return delta_v

def flatten_lon_lat(datain,name='sla',time=True):
    lon,lat = np.meshgrid(datain.lon,datain.lat)   
    flat_x = sl(datain).flat_x
    coords={'lon': (['x'], lon.flatten()),'lat': (['x'], lat.flatten())}
    if time:
        coords['time'] = datain.time.values
        var_dict = {name: (['time','x'],  flat_x)}
    else:
        var_dict = {name: (['x'],  flat_x)}        

    ds = xr.Dataset(var_dict,coords=coords)  
    return ds   

def divide_vals(data_in,fac=1000.):

    for var in list(data_in.data_vars):
        if np.issubdtype(data_in[var].dtype, np.floating):
            data_in[var] = data_in[var]/fac
    return data_in

def esitmate_2d_GP(y,sigma,X_all,scale = 150,iterations=20,Z_alt=[]):
    # Define the kernel: RBF (Radial Basis Function) with a constant term
    X=X_all
    x_pred = np.linspace(X[:,0].min()-2, X[:,0].max()+2, scale)
    y_pred = np.linspace(X[:,1].min()-2, X[:,1].max()+2, scale)
    X_pred, Y_pred = np.meshgrid(x_pred, y_pred)
    Z_pred = np.column_stack([X_pred.ravel(), Y_pred.ravel()])

    Y_means = []
    Y_means_target = []    
    for rand_state in range(iterations):
        X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size=0.25, random_state=rand_state)

        kernel = C(1.0) * RBF(length_scale=[1,1], length_scale_bounds=(0.1, 3)) + WhiteKernel(noise_level=2)

        # Create Gaussian Process Regressor with input uncertainty (alpha)
        gp = GaussianProcessRegressor(kernel=kernel, alpha=X_train[:,2:].flatten()**2, n_restarts_optimizer=10)
        # Fit the model
        gp.fit(X_train[:,:2], y_train)
        # Create a 2D grid for predictions
        # Predict mean and standard deviation
        y_mean, y_std = gp.predict(Z_pred, return_std=True)
        # Reshape outputs
        Y_mean = y_mean.reshape(scale, scale)
        Y_std = y_std.reshape(scale, scale)
        Y_means.append(Y_mean)
        if len(Z_alt) >0:
            y_meant, y_stdt = gp.predict(Z_alt, return_std=True)
            Y_means_target.append(y_meant)
    return np.array(Y_means),np.array(Y_means_target)



def plot_map_ax_mapping(ax,ds,region='world',msize=150,msize_frac = 0.6,scalecolor=False,scaler_factor=1,
                        label='a)',color_map=mpl_cm.get_cmap('brewer_RdBu_11',9),
                        proj = ccrs.PlateCarree(),minv = -4.5,maxv = 4.5,
                        land_after=False,set_extend=True,zorder=0,
                        edgecolor='grey',alpha=1,alpha_overlay=0.5,aspect=1.3,extend=[-180,180,-90,90],features=[],
                        gltop=True,glleft=True,glbottom=True,glright=True,overlay_ocean=False,
                        land_facecolor='gainsboro',ocean_edgecolor='k',rasterize=False,
                        resolution = '10m',draw_gridlines=True,scatter_kws={}):    

    
    if region =='world':
        extend=[-180,180,-75,75]
        if proj == ccrs.Robinson():
            extend=[-180,180,-90,90]        
        
    if region =='europe':
        extend=[-10,30,34,67]    
    elif region =='na':
        extend=[-150,-50,10,75]
    elif region =='japan':
        extend=[124,144,25,49]    
    elif region =='AUS':
        extend=[90,180,-45,24]     
    elif region=='custom':
        extend=extend

    land_50m = cfeature.NaturalEarthFeature('physical', 'land', resolution,
                                    edgecolor='face',
                                    facecolor=land_facecolor)#'#f7f7f7')#cfeature.COLORS['land'])    
    
    ax.add_feature(land_50m,zorder=-1)
    #ax.coastlines('10m')

    #ax.set_aspect(aspect=1)

    
    


    lon=ds.lon.values
    lat=ds.lat.values
    data=ds.values

    s=np.zeros(len(data))
    how='sqrt'
    factor=2
    if scalecolor:
        data_scale = data/np.nanstd(data)    
        s=abs(data_scale)*factor
        s[s<scaler_factor] =scaler_factor

    else:
        s=1


    im = ax.scatter(lon,lat,c=data,s=s*msize,edgecolor=edgecolor,
                            vmin=minv,vmax=maxv,cmap=color_map,
                    transform=ccrs.Geodetic(),zorder=zorder,alpha=alpha,**scatter_kws)

    ax.scatter(lon,lat,c=data,s=s*msize_frac*msize,alpha=alpha_overlay,
                            vmin=minv,vmax=maxv,cmap=color_map,
                    transform=ccrs.Geodetic(),zorder=zorder,**scatter_kws)

    if region =='world':   
        ax.scatter([-180,180],[0,0],c=[0,0],s=0.0001,alpha=0,
                                vmin=minv,vmax=maxv,
                        transform=ccrs.Geodetic(),zorder=zorder,**scatter_kws) 
        
    if overlay_ocean:
        ocean_50m = cfeature.NaturalEarthFeature('physical', 'ocean', resolution,
                                    edgecolor=ocean_edgecolor,
                                    facecolor='white')#'#f7f7f7')#cfeature.COLORS['land'])      
        ax.add_feature(ocean_50m,facecolor='white', zorder=2, edgecolor=ocean_edgecolor)     
    for feature in features:
        if feature != None:
            feature_50m = cfeature.NaturalEarthFeature('physical', feature, resolution,
                                        edgecolor='k',
                                        facecolor='white')#'#f7f7f7')#cfeature.COLORS['land'])      
            ax.add_feature(feature_50m,facecolor='white', zorder=2, edgecolor='k')               
        

    if region =='world':    
        if set_extend:
            print('set_extend')
            xmin=75
            extend=[-179.99999,179.99999,-xmin,xmin] 
            ax.set_extent(extend)

        extend=[-180,180,-xmin,xmin]
    else:
        ax.set_extent(extend)
    xticks,yticks=plt_make_ticks(extend[2:])   
    if draw_gridlines:
        gl=ax.gridlines(draw_labels=True,xlocs=xticks, ylocs=yticks, alpha=0.25,zorder=10)
        gl=gl_props(gl,0.15)

        gl.xlabels_top = gltop
        gl.ylabels_left = glleft
        gl.xlabels_bottom = glbottom
        gl.ylabels_right = glright

    
    ax.set_title(label,loc='left', y=1.08)
    ax.set_aspect(aspect)
    if land_after:
        ax.add_feature(land_50m,zorder=2)
    return ax,im    


def lonlat_to_xyz_km(lon_deg, lat_deg, R=6371.0088):
    lon = np.deg2rad(lon_deg)
    lat = np.deg2rad(lat_deg)
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R * np.sin(lat)
    return np.column_stack([x, y, z])


def bootstrap_wavg(dat,weights,it=100, test_size=0.5):
    all_means = []
    for i in range(it):
        X_train, X_test, y_train, y_test = train_test_split(dat, weights, test_size=test_size, random_state=i)
        mean_,w_std = weighted_avg_and_std(X_train, y_train)
        all_means.append(mean_)
    return np.array(all_means)

def bootstrap_wavg_un(dat, weights, stds, it=100, test_size=0.5, seed=0):
    """
    dat:     1D array of data values
    weights: 1D array of weights (same length)
    stds:    1D array of per-point std devs for dat (same length)
    it:      number of bootstrap iterations
    """
    dat     = np.asarray(dat)
    weights = np.asarray(weights)
    stds    = np.asarray(stds)

    if not (len(dat) == len(weights) == len(stds)):
        raise ValueError("dat, weights, stds must have the same length")

    rng = np.random.default_rng(seed)
    means = np.empty(it, dtype=float)

    idx_all = np.arange(len(dat))

    for i in range(it):
        # split on indices so we can align stds with sampled points
        idx_train, _ = train_test_split(idx_all, test_size=test_size, random_state=seed + i, shuffle=True)

        # perturb the training data with per-point Gaussian noise
        noise = rng.normal(loc=0.0, scale=stds[idx_train])
        X_train = dat[idx_train] + noise
        y_train = weights[idx_train]

        mean_, w_std = weighted_avg_and_std(X_train, y_train)  # your existing function
        means[i] = mean_

    return means


def fit_johnson_su(percentiles, values, make_plots=True):

    # objective: match quantiles
    def objective(params):
        gamma, delta, loc, scale = params
        if scale <= 0 or delta <= 0:
            return np.inf
        est = johnsonsu.ppf(percentiles, gamma, delta, loc=loc, scale=scale)
        return np.sum((est - values)**2)

    # initial guess
    initial = [0.1, 1.0, values[2], (values[4]-values[3])/3]

    res = minimize(objective, initial, method="Nelder-Mead")
    gamma_hat, delta_hat, loc_hat, scale_hat = res.x

    estimated = johnsonsu.ppf(percentiles, gamma_hat, delta_hat,
                              loc=loc_hat, scale=scale_hat)

    print("Johnson SU parameters:")
    print(f"  gamma = {gamma_hat:.3f}")
    print(f"  delta = {delta_hat:.3f}")
    print(f"  loc   = {loc_hat:.3f}")
    print(f"  scale = {scale_hat:.3f}")

    return gamma_hat, delta_hat, loc_hat, scale_hat, estimated