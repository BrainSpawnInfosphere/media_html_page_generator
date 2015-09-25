

def write_css(path = './'):
	content = """
div.img {
    margin: 1px;
    padding: 0px;
    float: left;
    text-align: center;
}	

div.img img {
    display: inline;
    margin: 0px;
    border: 0px solid #ffffff;
}

h3 {
	text-align: center;
}

i { 
    font-style: normal;
}

.mpaa_rating {
	font-family: serif;
	border-style: solid;
	border-width: 2px;
	border-radius: 5px;
	background-color: white;
	padding: 0px 3px 0px 3px;
	font-size: 20px;
}

.rt_rating {
	position: relative;
}
.rating {
	font-family: serif;
	position: absolute;
	top: 70%;
	left: 25%;
	color: white;
	background-color: gray;
	border-style: solid;
	border-width: 0px;
	border-radius: 25px;
	padding: 0px 2px 0px 2px;

}

.tagline{
	width:100%;
    text-align:center;
    margin: 5px;
}
.container{
	width:100%;
    text-align:center;
}
.left {
	float: left;
}
.right {
	float: right;
}
.center {
	margin:0 auto;
	width:100px;
}
	"""
	if not path[-1] == '/': path += '/'
	filename = path + 'mystyle.css'	
	f = open(filename,'w')
	f.write(content)
	f.close()
