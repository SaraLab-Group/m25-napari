main();
function main(){
	//Select the ROI with Bead
	run("Clear Results");
	stack1=getImageID();
	waitForUser("Draw Box Around Bead");
	run("Duplicate...", "title=bead duplicate");
	//Find the Center of the bead
	run("Z Project...", "projection=[Max Intensity]");
	rename("max_projection");
	coords = findCenter();
	getDimensions(w, h, channels, slices, frames);
	voxel=50;
	if(w!=voxel || h!=voxel){
		makeRectangle(coords[0]-(voxel/2),coords[1]-(voxel/2),voxel,voxel);
		run("Duplicate...", "title=70x70_max duplicate");
		coords_70x70 = findCenter();
		close("70x70_max");
		selectWindow("bead");
		makeRectangle(coords[0]-(voxel/2),coords[1]-(voxel/2),voxel,voxel);
		run("Duplicate...", "title=70x70 duplicate");
	}
	close("max_projection");
	//Get the Center of the newly cropped
	selectWindow("70x70");
	getDimensions(w, h, channels, slices, frames);
	Stack.getPosition(channel, slice, frame);
	print("   Channels: "+channels);
	print("   Slices: "+slices);
	print("   Frames: "+frames);

	
	r_band=1;
	run("Set Measurements...", "area mean standard min redirect=None decimal=3");
 	f = File.open(""); // display file open dialog
	//Print for 25 channels
	String.resetBuffer;
	for(i=1;i<=channels;i++){
		String.append("C"+ i + ",");		
	}
	str_channel=String.buffer;
	print(f,str_channel);
	String.resetBuffer;
	
	if (channels>1) {
		zCount=0;
		for (i=1; i<=slices; i++) {
//				print(f,"\t");
				Stack.setSlice(i);
				run("Clear Results");
				String.resetBuffer;
				
			for(j=1;j<=channels;j++){
				Stack.setChannel(j);
				radius=(r_band);
				makeOval(coords_70x70[0]-radius,coords_70x70[1]-radius,radius*2,radius*2);
				run("Make Band...", "band="+r_band);
				run("Measure");
				updateResults();
				
				value=d2s(getResult("Mean", j-1),3) + ",";
				String.append(value);
			}
			average=String.buffer;
			print(f,average);
		}
	}
}


function findCenter(){
	id=getImageID();
	run("Select None");
	run("Clear Results");
	run("Duplicate...", "duplicate");
	rename("threshold_mask");
	thresholding(99.5);
	run("Convert to Mask", "method=Default background=Dark black");
	run("Analyze Particles...", "size=10-Infinity display clear stack");
	close("threshold_mask");
	a=newArray(2);
	for (i = 0; i < nResults(); i++) {
	    x += getResult('X', i);
	    y += getResult('Y', i);
	}
	x_avg= x/(nResults());
	y_avg= y/(nResults());
	updateResults();
	a[0]=x_avg;
	a[1]=y_avg;
	selectImage(id);
//	Array.print(a);
	return a;
}

function thresholding(percentage){
	nBins = 256;
	run("Set Measurements...", "area mean standard min centroid center fit redirect=None decimal=3");
	getDimensions(width, height, channels, slices, frames);
	for(i=1;i<=channels;i++){
		Stack.setPosition(i, 1, 1);
		resetMinAndMax(); 
	}
	getHistogram(values, counts, nBins); 
	max = pow(2, bitDepth());
//	print(max);
//	// find culmulative sum 
	nPixels = 0; 
	for (i = 0; i<counts.length; i++){ 
	  nPixels += counts[i]; 
	}
	nBelowThreshold = nPixels * percentage / 100.0; 
	sum = 0; 
	for (i = 0; i<counts.length; i++) { 
	  sum = sum + counts[i]; 
//	  print(sum + "   "+ nBelowThreshold+" "+ values[i]+" "+max);
	  if (sum >= nBelowThreshold) { 
	    setThreshold(values[i], max); 
		    print(values[i]+"-"+max+": "+sum/nPixels*100.0+"%"); 
	    i = 99999999;//break 
	  } 
	}
}
