import _ from 'lodash';

function component() {
   var element = document.createElement('div')
   element.innerHTML = _.join(['Hello','world','!!'], ' ');

   return element;
}

document.body.appendChild(component());

/* ********************OL************************* */
//import 'ol/ol.css';
import {Map, View} from 'ol';

import Feature from 'ol/Feature';

import Point from 'ol/geom/Point';
//import TileJSON from 'ol/source/TileJSON';
import {OSM, Stamen} from 'ol/source';
import TileWMS from 'ol/source/TileWMS';
//import OSM from 'ol/source/OSM';
import VectorSource from 'ol/source/Vector';

import {Icon, Style, Circle as CircleStyle, Fill, Stroke, Text} from 'ol/style';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';

import GeoJSON from 'ol/format/GeoJSON';
import GPX from 'ol/format/GPX';

import {useGeographic} from 'ol/proj';

useGeographic();

//////////////////////////////////////



////////////////////////////////////

var style = {
  'Point': new Style({
    image: new CircleStyle({
      fill: new Fill({
        color: 'rgba(255,255,0,0.4)',
      }),
      radius: 5,
      stroke: new Stroke({
        color: 'red',
        width: 2,
      }),
    }),
  }),
  'LineString': new Style({
    stroke: new Stroke({
      color: '#f00',
      width: 3,
    }),
  }),
  'MultiLineString': new Style({
    stroke: new Stroke({
      color: '#c008cc',
      width: 3,
    }),
  }),
  'Text': new Text({
      font: 'bold 11px "Open Sans", "Arial Unicode MS", "sans-serif"',
      placement: 'point',
      fill: new Fill({color: '#fff'}),
      stroke: new Stroke({color: '#000', width: 2}),
  }),

  };
  
//////////////////////GeoJSON Layer///////////////////////////////

var pointLayer = new VectorLayer({
  source: new VectorSource({
    url: `getPoints`,
    format: new GeoJSON(),
  }),
  style: function (feature) {
  return style[feature.getGeometry().getType()];
  },
});

var testPointLayer = new VectorLayer({
  source: new VectorSource({
    url: 'static/data/points.geojson',
  //  url: `getPoints`,
    format: new GeoJSON(),
  }),
  style: function (feature) {
    return style[feature.getGeometry().getType()];
  },
});

//////////////////////////////////// Layer ////////////////////////////
var baselayer = new TileLayer({
    source: new OSM()
    });

var stamenLayer = new TileLayer({
    source: new Stamen({
    layer: 'toner',
      }),
    });

var regenradar = new TileLayer({
    source: new TileWMS({
    url: 'https://maps.dwd.de/geoserver/wms',
    params: {'LAYERS': 'dwd:Niederschlagsradar', 'TILED': true},
    serverType: 'geoserver',
    // Countries have transparency, so do not fade tiles:
    opacity: 0.5,
  }),
});

  //  https://maps.dwd.de/geoserver/ows?

var iconFeature = new Feature({
    geometry: new Point([0, 0]),
    name: 'Null Island',
    population: 4000,
    rainfall: 500,
    });

  var newIconFeature = new Feature({
    geometry: new Point([9.5, 51.3]),
    name: 'Kassel Island',
    population: 4000,
    rainfall: 500,
    });

var vectorSource = new VectorSource({
    features: [iconFeature, newIconFeature],
    });

var vectorLayer = new VectorLayer({
    source: vectorSource,
    style: function (feature) {
      return style[feature.getGeometry().getType()];
      },
    });

var gpxLayer = new VectorLayer({
    source: new VectorSource({
      url: 'static/data/track_harz.gpx',
      format: new GPX(),
    }),
    style: function (feature) {
      return style[feature.getGeometry().getType()];
    },
  });
    
////////////////////////////////

var map = new Map({
  target: 'map',
  layers: [
    /* baselayer,*/ stamenLayer, regenradar, /*vectorLayer,*/ gpxLayer, pointLayer, //testPointLayer
  ],
  view: new View({
    center: [9, 50],
    zoom: 5
  })
});

map.on('singleclick', function (evt) {
  console.log(evt.coordinate);
  var xy = evt.coordinate;
//  console.log(xy);
  $.getJSON({
    url: `/savePoint/${xy[0]}/${xy[1]}/${$("#pointName").val()}/`,
    success: data => {
        console.log(data);
        location.reload();
    }
  }).error(function(jqXHR, textStatus, errorThrown) {
      console.log("error " + textStatus);
      console.log("incoming Text " + jqXHR.responseText);
  });
});

//////////////////////////////////////////////////// 

map.on('pointermove', showInfo);

const info = document.getElementById('info');
function showInfo(event) {
  const features = map.getFeaturesAtPixel(event.pixel);
  if (features.length == 0) {
    info.innerText = '';
    info.style.opacity = 0;
    return;
  }
  const properties = features[0].getProperties();
  info.innerText = JSON.stringify(properties['name'], null, 2);
  info.style.opacity = 1;
}

/*
var dict = {typename : "test" , content:"irgendwas"};

    $.ajax({
        type: "POST", 
        url: "http://192.168.3.45:2100/saveMyJson", //localhost Flask
        data : JSON.stringify(dict),
        contentType: "application/json",
    });
*/