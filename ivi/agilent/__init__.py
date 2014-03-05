"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

# Oscilloscopes
# InfiniiVision 2000A
from .agilentDSOX2002A import agilentDSOX2002A
from .agilentDSOX2004A import agilentDSOX2004A
from .agilentDSOX2012A import agilentDSOX2012A
from .agilentDSOX2014A import agilentDSOX2014A
from .agilentDSOX2022A import agilentDSOX2022A
from .agilentDSOX2024A import agilentDSOX2024A
from .agilentMSOX2002A import agilentMSOX2002A
from .agilentMSOX2004A import agilentMSOX2004A
from .agilentMSOX2012A import agilentMSOX2012A
from .agilentMSOX2014A import agilentMSOX2014A
from .agilentMSOX2022A import agilentMSOX2022A
from .agilentMSOX2024A import agilentMSOX2024A
# InfiniiVision 3000A
from .agilentDSOX3012A import agilentDSOX3012A
from .agilentDSOX3014A import agilentDSOX3014A
from .agilentDSOX3024A import agilentDSOX3024A
from .agilentDSOX3032A import agilentDSOX3032A
from .agilentDSOX3034A import agilentDSOX3034A
from .agilentDSOX3052A import agilentDSOX3052A
from .agilentDSOX3054A import agilentDSOX3054A
from .agilentDSOX3102A import agilentDSOX3102A
from .agilentDSOX3104A import agilentDSOX3104A
from .agilentMSOX3012A import agilentMSOX3012A
from .agilentMSOX3014A import agilentMSOX3014A
from .agilentMSOX3024A import agilentMSOX3024A
from .agilentMSOX3032A import agilentMSOX3032A
from .agilentMSOX3034A import agilentMSOX3034A
from .agilentMSOX3052A import agilentMSOX3052A
from .agilentMSOX3054A import agilentMSOX3054A
from .agilentMSOX3102A import agilentMSOX3102A
from .agilentMSOX3104A import agilentMSOX3104A
# InfiniiVision 4000A
from .agilentDSOX4022A import agilentDSOX4022A
from .agilentDSOX4024A import agilentDSOX4024A
from .agilentDSOX4032A import agilentDSOX4032A
from .agilentDSOX4034A import agilentDSOX4034A
from .agilentDSOX4052A import agilentDSOX4052A
from .agilentDSOX4054A import agilentDSOX4054A
from .agilentDSOX4104A import agilentDSOX4104A
from .agilentDSOX4154A import agilentDSOX4154A
from .agilentMSOX4022A import agilentMSOX4022A
from .agilentMSOX4024A import agilentMSOX4024A
from .agilentMSOX4032A import agilentMSOX4032A
from .agilentMSOX4034A import agilentMSOX4034A
from .agilentMSOX4052A import agilentMSOX4052A
from .agilentMSOX4054A import agilentMSOX4054A
from .agilentMSOX4104A import agilentMSOX4104A
from .agilentMSOX4154A import agilentMSOX4154A
# InfiniiVision 6000A
from .agilentDSO6012A import agilentDSO6012A
from .agilentDSO6014A import agilentDSO6014A
from .agilentDSO6032A import agilentDSO6032A
from .agilentDSO6034A import agilentDSO6034A
from .agilentDSO6052A import agilentDSO6052A
from .agilentDSO6054A import agilentDSO6054A
from .agilentDSO6102A import agilentDSO6102A
from .agilentDSO6104A import agilentDSO6104A
from .agilentMSO6012A import agilentMSO6012A
from .agilentMSO6014A import agilentMSO6014A
from .agilentMSO6032A import agilentMSO6032A
from .agilentMSO6034A import agilentMSO6034A
from .agilentMSO6052A import agilentMSO6052A
from .agilentMSO6054A import agilentMSO6054A
from .agilentMSO6102A import agilentMSO6102A
from .agilentMSO6104A import agilentMSO6104A
# InfiniiVision 7000A
from .agilentDSO7012A import agilentDSO7012A
from .agilentDSO7014A import agilentDSO7014A
from .agilentDSO7032A import agilentDSO7032A
from .agilentDSO7034A import agilentDSO7034A
from .agilentDSO7052A import agilentDSO7052A
from .agilentDSO7054A import agilentDSO7054A
from .agilentDSO7104A import agilentDSO7104A
from .agilentMSO7012A import agilentMSO7012A
from .agilentMSO7014A import agilentMSO7014A
from .agilentMSO7032A import agilentMSO7032A
from .agilentMSO7034A import agilentMSO7034A
from .agilentMSO7052A import agilentMSO7052A
from .agilentMSO7054A import agilentMSO7054A
from .agilentMSO7104A import agilentMSO7104A
# InfiniiVision 7000B
from .agilentDSO7012B import agilentDSO7012B
from .agilentDSO7014B import agilentDSO7014B
from .agilentDSO7032B import agilentDSO7032B
from .agilentDSO7034B import agilentDSO7034B
from .agilentDSO7052B import agilentDSO7052B
from .agilentDSO7054B import agilentDSO7054B
from .agilentDSO7104B import agilentDSO7104B
from .agilentMSO7012B import agilentMSO7012B
from .agilentMSO7014B import agilentMSO7014B
from .agilentMSO7032B import agilentMSO7032B
from .agilentMSO7034B import agilentMSO7034B
from .agilentMSO7052B import agilentMSO7052B
from .agilentMSO7054B import agilentMSO7054B
from .agilentMSO7104B import agilentMSO7104B
# Infiniium 90000A
from .agilentDSO90254A import agilentDSO90254A
from .agilentDSO90404A import agilentDSO90404A
from .agilentDSO90604A import agilentDSO90604A
from .agilentDSO90804A import agilentDSO90804A
from .agilentDSO91204A import agilentDSO91204A
from .agilentDSO91304A import agilentDSO91304A
from .agilentDSA90254A import agilentDSA90254A
from .agilentDSA90404A import agilentDSA90404A
from .agilentDSA90604A import agilentDSA90604A
from .agilentDSA90804A import agilentDSA90804A
from .agilentDSA91204A import agilentDSA91204A
from .agilentDSA91304A import agilentDSA91304A
# Infiniium 90000X
from .agilentDSOX91304A import agilentDSOX91304A
from .agilentDSOX91604A import agilentDSOX91604A
from .agilentDSOX92004A import agilentDSOX92004A
from .agilentDSOX92504A import agilentDSOX92504A
from .agilentDSOX92804A import agilentDSOX92804A
from .agilentDSOX93204A import agilentDSOX93204A
from .agilentDSAX91304A import agilentDSAX91304A
from .agilentDSAX91604A import agilentDSAX91604A
from .agilentDSAX92004A import agilentDSAX92004A
from .agilentDSAX92504A import agilentDSAX92504A
from .agilentDSAX92804A import agilentDSAX92804A
from .agilentDSAX93204A import agilentDSAX93204A
from .agilentMSOX91304A import agilentMSOX91304A
from .agilentMSOX91604A import agilentMSOX91604A
from .agilentMSOX92004A import agilentMSOX92004A
from .agilentMSOX92504A import agilentMSOX92504A
from .agilentMSOX92804A import agilentMSOX92804A
from .agilentMSOX93204A import agilentMSOX93204A

# Spectrum Analyzers
# 859x series
from .agilent8590L import agilent8590L
from .agilent8591C import agilent8591C
from .agilent8591E import agilent8591E
from .agilent8593E import agilent8593E
from .agilent8593EM import agilent8593EM
from .agilent8594E import agilent8594E
from .agilent8594EM import agilent8594EM
from .agilent8594L import agilent8594L
from .agilent8594Q import agilent8594Q
from .agilent8595E import agilent8595E
from .agilent8595EM import agilent8595EM
from .agilent8596E import agilent8596E
from .agilent8596EM import agilent8596EM

# Digital Multimeters
from .agilent34401A import agilent34401A
from .agilent34410A import agilent34410A
from .agilent34411A import agilent34411A

# DC Power Supplies
# 603xA
from .agilent6030A import agilent6030A
from .agilent6031A import agilent6031A
from .agilent6032A import agilent6032A
from .agilent6033A import agilent6033A
from .agilent6035A import agilent6035A
from .agilent6038A import agilent6038A
# E3600A
from .agilentE3631A import agilentE3631A
from .agilentE3632A import agilentE3632A
from .agilentE3633A import agilentE3633A
from .agilentE3634A import agilentE3634A
from .agilentE3640A import agilentE3640A
from .agilentE3641A import agilentE3641A
from .agilentE3642A import agilentE3642A
from .agilentE3643A import agilentE3643A
from .agilentE3644A import agilentE3644A
from .agilentE3645A import agilentE3645A
from .agilentE3646A import agilentE3646A
from .agilentE3647A import agilentE3647A
from .agilentE3648A import agilentE3648A
from .agilentE3649A import agilentE3649A

# RF Power Meters
from .agilent436A import agilent436A
from .agilent437B import agilent437B

# RF Signal Generators
from .agilent8642A import agilent8642A
from .agilent8642B import agilent8642B

# Optical spectrum analyzers
from .agilent86140B import agilent86140B
from .agilent86141B import agilent86141B
from .agilent86142B import agilent86142B
from .agilent86144B import agilent86144B
from .agilent86145B import agilent86145B
from .agilent86146B import agilent86146B

# Optical attenuators
from .agilent8156A import agilent8156A


