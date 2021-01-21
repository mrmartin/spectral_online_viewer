from flask import Flask, request, render_template
from flask import send_file
import numpy as np
import imageio

app = Flask(__name__)

wavelengths = [397.32, 400.20, 403.09, 405.97, 408.85, 411.74, 414.63, 417.52, 420.40, 423.29, 426.19, 429.08, 431.97, 434.87, 437.76, 440.66, 443.56, 446.45, 449.35, 452.25, 455.16, 458.06, 460.96, 463.87, 466.77, 469.68, 472.59, 475.50, 478.41, 481.32, 484.23, 487.14, 490.06, 492.97, 495.89, 498.80, 501.72, 504.64, 507.56, 510.48, 513.40, 516.33, 519.25, 522.18, 525.10, 528.03, 530.96, 533.89, 536.82, 539.75, 542.68, 545.62, 548.55, 551.49, 554.43, 557.36, 560.30, 563.24, 566.18, 569.12, 572.07, 575.01, 577.96, 580.90, 583.85, 586.80, 589.75, 592.70, 595.65, 598.60, 601.55, 604.51, 607.46, 610.42, 613.38, 616.34, 619.30, 622.26, 625.22, 628.18, 631.15, 634.11, 637.08, 640.04, 643.01, 645.98, 648.95, 651.92, 654.89, 657.87, 660.84, 663.81, 666.79, 669.77, 672.75, 675.73, 678.71, 681.69, 684.67, 687.65, 690.64, 693.62, 696.61, 699.60, 702.58, 705.57, 708.57, 711.56, 714.55, 717.54, 720.54, 723.53, 726.53, 729.53, 732.53, 735.53, 738.53, 741.53, 744.53, 747.54, 750.54, 753.55, 756.56, 759.56, 762.57, 765.58, 768.60, 771.61, 774.62, 777.64, 780.65, 783.67, 786.68, 789.70, 792.72, 795.74, 798.77, 801.79, 804.81, 807.84, 810.86, 813.89, 816.92, 819.95, 822.98, 826.01, 829.04, 832.07, 835.11, 838.14, 841.18, 844.22, 847.25, 850.29, 853.33, 856.37, 859.42, 862.46, 865.50, 868.55, 871.60, 874.64, 877.69, 880.74, 883.79, 886.84, 889.90, 892.95, 896.01, 899.06, 902.12, 905.18, 908.24, 911.30, 914.36, 917.42, 920.48, 923.55, 926.61, 929.68, 932.74, 935.81, 938.88, 941.95, 945.02, 948.10, 951.17, 954.24, 957.32, 960.40, 963.47, 966.55, 969.63, 972.71, 975.79, 978.88, 981.96, 985.05, 988.13, 991.22, 994.31, 997.40, 1000.49, 1003.58]
#remove last few wavelengths because they are only noise...?
wavelengths=wavelengths[:-4]

@app.route("/banany/")
def hello():
    if request.args.get('filenum'):
        filenum = request.args.get('filenum')
    else:
        filenum = 172
    if request.args.get('red_range'):
        red_range = request.args.get('red_range')
        from_red = wavelengths.index(float(red_range[0:red_range.find(";")]))
        to_red = wavelengths.index(float(red_range[red_range.find(";")+1:]))
    else:
        from_red = 100
        to_red = 161

    if request.args.get('green_range'):
        green_range = request.args.get('green_range')
        from_green = wavelengths.index(float(green_range[0:green_range.find(";")]))
        to_green = wavelengths.index(float(green_range[green_range.find(";")+1:]))
    else:
        from_green = 61
        to_green = 77

    if request.args.get('blue_range'):
        blue_range = request.args.get('blue_range')
        from_blue = wavelengths.index(float(blue_range[0:blue_range.find(";")]))
        to_blue = wavelengths.index(float(blue_range[blue_range.find(";")+1:]))
    else:
        from_blue = 0
        to_blue = 19

    filenames = [160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 177, 181, 184]
    return render_template('banany.html', filenum=int(filenum), from_red=from_red, to_red=to_red, from_green=from_green, to_green=to_green, from_blue=from_blue, to_blue=to_blue, wavelengths=wavelengths, filenames=filenames)

@app.route("/banany/spectral_demo/<filenum>/<from_red>/<to_red>/<from_green>/<to_green>/<from_blue>/<to_blue>")
def spectral_demo(filenum, from_red, to_red, from_green, to_green, from_blue, to_blue):
    #if request.args.get('filenum'):
    #   filenum = request.args.get('filenum')
    #else:
    #    filenum = 140
    filenum = int(filenum)
    rawfile = '/mnt/matylda1/kolarmartin/Specim_IQ/smd/'+str(filenum)+'/results/REFLECTANCE_'+str(filenum)+'.dat'
    print(rawfile)

    f = open(rawfile, "r")
    im = np.fromfile(f, dtype=np.float32)
    im = np.reshape(im,[512, 204, 512])
    im = np.transpose(im,(2,0,1))[:,::-1,:] #reshape to 512x512x204 with correct orientation
    #remove last few wavelengths because they are only noise...?
    im = im[:,:,:len(wavelengths)]

    from_red = int(from_red)
    to_red = int(to_red)
    red_image = np.sum(im[:,:,from_red:to_red+1],axis=2);
    red_image = red_image/np.max(red_image)

    from_green = int(from_green)
    to_green = int(to_green)
    green_image = np.sum(im[:,:,from_green:to_green+1],axis=2);
    green_image = green_image/np.max(green_image)

    from_blue = int(from_blue)
    to_blue = int(to_blue)
    blue_image = np.sum(im[:,:,from_blue:to_blue+1],axis=2);
    blue_image = blue_image/np.max(blue_image)
    imageio.imwrite('current_spectral_banan.jpg', np.dstack((red_image, green_image, blue_image)))

    filename = 'current_spectral_banan.jpg'
    return send_file(filename, mimetype='image/jpeg')

@app.route("/banany/point_spectrum/filenum=<filenum>&x=<x>&y=<y>")
def spectral_graph(filenum, x, y):
    filenum = int(filenum)
    rawfile = '/mnt/matylda1/kolarmartin/Specim_IQ/smd/'+str(filenum)+'/results/REFLECTANCE_'+str(filenum)+'.dat'
    print(rawfile)

    f = open(rawfile, "r")
    im = np.fromfile(f, dtype=np.float32)
    im = np.reshape(im,[512, 204, 512])
    im = np.transpose(im,(2,0,1))[:,::-1,:] #reshape to 512x512x204 with correct orientation
    #remove last few wavelengths because they are only noise...?
    im = im[:,:,:len(wavelengths)]

    x=int(x)
    y=int(y)

    from matplotlib import pyplot as plt
    plt.figure(figsize=(10, 4))

    ax1=plt.subplot(1, 2, 2)
    plt.plot(wavelengths,im[y,x,:]/np.max(im[y,x,:]))
    plt.xlabel('wavelength')
    plt.ylabel('relative intensity')
    plt.title('measured spectrum at ('+str(x)+","+str(y)+") of file #"+str(filenum))

    ax2=plt.subplot(1, 2, 1)
    show_im = np.sum(im,axis=2)
    plt.imshow(show_im,cmap="gray")
    plt.scatter(x, y, s=200, marker="x", color='white')
    plt.axis('off')

    plt.savefig('current_spectral_banan_graph.png')

    filename = 'current_spectral_banan_graph.png'
    return send_file(filename, mimetype='image/png')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
