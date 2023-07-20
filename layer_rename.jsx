#target photoshop
app.bringToFront();

var layers = activeDocument.layers;

for (var i = 0; i < layers.length; i++) {
  if(layers[i].name[0] == '[')
		layers[i].name = layers[i].name.replace(".png", "");
	else
		layers[i].name = "@(" + layers[i].name.replace(".png", "") + ")";
}