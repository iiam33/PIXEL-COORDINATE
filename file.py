from wand.image import Image 

with Image(filename ='SampleImage.png') as Sampleimg:  
    Sampleimg.format = 'tiff' 
    Sampleimg.save(filename ='SampleImage.tiff')