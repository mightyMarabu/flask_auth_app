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
//import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import Feature from 'ol/Feature';
//import Map from 'ol/Map';
import Overlay from 'ol/Overlay';
import Point from 'ol/geom/Point';
import TileJSON from 'ol/source/TileJSON';
import VectorSource from 'ol/source/Vector';
//import View from 'ol/View';
import {Icon, Style} from 'ol/style';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';

var baselayer = new TileLayer({
    source: new OSM()
    });

var iconFeature = new Feature({
    geometry: new Point([0, 0]),
    name: 'Null Island',
    population: 4000,
    rainfall: 500,
    });

var vectorSource = new VectorSource({
    features: [iconFeature],
    });

var vectorLayer = new VectorLayer({
    source: vectorSource,
    });

const map = new Map({
  target: 'map',
  layers: [
  vectorLayer, baselayer
  ],
  view: new View({
    center: [0, 0],
    zoom: 0
  })
});