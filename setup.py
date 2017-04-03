from setuptools import setup, find_packages                                    
                                                                               
setup(                                                                         
    name='fronde',                                                              
    version='1.0',                                                             
    install_requires=['numpy','scipy'],
    packages=find_packages(),                                                  
    zip_safe=False,                                                            
) 
