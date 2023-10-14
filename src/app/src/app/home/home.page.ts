import { Component, ElementRef } from '@angular/core';
import { formatDate } from '@angular/common';
import { LoadingController, Platform, ToastController } from '@ionic/angular';
import { Geolocation } from '@capacitor/geolocation';
import { BlockageService } from 'src/services/blockage.service';
import { SimulationService } from 'src/services/simulation.service';
import { RoutesService } from 'src/services/routes.service';

import * as L from "leaflet";


@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})

export class HomePage {
  // this latlng is used for viewport centering and navigation
  initLat = 0;
  initLng = 0;

  myMap: L.Map | undefined;

  locationIcon = L.divIcon({
    className: "location-marker",
    html: `<ion-icon name="location"/>`,

    iconAnchor: [20, 40],
    iconSize: [40, 40],
    // popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
  });

  barrierIcon = L.icon({
    iconUrl: './assets/barrier-32.png',

    iconSize:     [32, 32], // size of the icon
    iconAnchor:   [16, 32], // point of the icon which will correspond to marker's location
    popupAnchor:  [0, -32] // point from which the popup should open relative to the iconAnchor
  });

  // this latlng is for marking and reporting blockages
  focusLocationExists: boolean = false;
  focusLocationMark: L.Marker | undefined;
  focusLocationLat: any;
  focusLocationLng: any;

  // list of blockages in the current area
  blockagesNearby: any[] = [];
  blockagesMarksMap = new Map<number, L.Marker>();

  constructor(
    private loadingCtrl: LoadingController,
    private blockageService: BlockageService,
    private simulationService: SimulationService,
    private routesService: RoutesService,
    private elementRef: ElementRef,
    private toastController: ToastController,
    public platform: Platform
  ) {}

  ionViewDidEnter() {
    this.loadMap();
  }

  // search item was clicked
  onsSearchResultSelected(selectedItem : any) {
    this.focusLocationLat = selectedItem.y;
    this.focusLocationLng = selectedItem.x;

    // pan to coordinates and drop a marker
    this.myMap?.setView([this.focusLocationLat, this.focusLocationLng], this.myMap.getZoom(), {
      animate: true,
      duration: 1,
      easeLinearity: 0.25
    });

    if (this.focusLocationMark) this.myMap?.removeLayer(this.focusLocationMark);
    this.focusLocationMark = L.marker([this.focusLocationLat, this.focusLocationLng], { icon: this.locationIcon }).addTo(this.myMap!);
  }

  // check if focusLocation has values
  hasFocusLocation() {
    if (this.focusLocationMark === undefined) return false;
    else return true;
  }

  // on initial load, load the map
  async loadMap() {
    let coordinates: any;
    if (!this.platform.is('cordova')) {
      const getCoords = async () => {
        const pos = await new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject);
        });
        return pos;
      };
      coordinates = await getCoords();
    } else {
      console.log('there');
      coordinates = await Geolocation.getCurrentPosition();
    }
    // console.log('Current position:', coordinates);

    this.initLat = coordinates.coords.latitude;
    this.initLng = coordinates.coords.longitude;

    this.myMap = L.map('map', {
      maxZoom: 18,
      minZoom: 8,
      zoomControl: false
    }).setView([this.initLat, this.initLng], 15);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(this.myMap);

    L.control.zoom({
      position: 'bottomleft'
    }).addTo(this.myMap);

    // allow marker drop on click around the map area
    this.myMap.on("click", e => {
      this.focusLocationLat = e.latlng.lat;
      this.focusLocationLng = e.latlng.lng;
      if (this.focusLocationMark) this.myMap?.removeLayer(this.focusLocationMark);
      this.focusLocationMark = L.marker([this.focusLocationLat, this.focusLocationLng], { icon: this.locationIcon }).addTo(this.myMap!); 
    });
  }

  // set map view to current location
  async viewCurrentLocation() {
    this.presentToast('Centering viewport around current location.', 'warning')

    let coordinates: any;
    if (!this.platform.is('cordova')) {
      const getCoords = async () => {
        const pos = await new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject);
        });
        return pos;
      };
      coordinates = await getCoords();
    } else {
      coordinates = await Geolocation.getCurrentPosition();
    }

    this.initLat = coordinates.coords.latitude;
    this.initLng = coordinates.coords.longitude;

    this.myMap?.setView([this.initLat, this.initLng], this.myMap.getZoom(), {
      animate: true,
      duration: 1,
      easeLinearity: 0.25
    });
  }

  // view blockages in the current map area
  viewBlockages() {
    this.presentToast('Displaying blockages in the area.', 'warning')

    // clear blockages currently displayed if there are any
    if (this.blockagesMarksMap.size > 0) this.clearBlockageMarkers();

    const popupOptions = {
      className: "blockage-popup"
    };

    // get the current bounds of the map
    this.initLat = this.myMap?.getCenter().lat ?? this.initLat;
    this.initLng = this.myMap?.getCenter().lng ?? this.initLng;
    const bounds = this.myMap?.getBounds();

    // get blockages from api
    this.blockageService.getBlockages(bounds!).subscribe( (res) => {
        this.blockagesNearby.push(...res.data);

        // set markers of the blockages
        this.blockagesNearby.forEach( (element) => {
          const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
          const formattedDate = formatDate(element.datetime_added, 'MMM d, y, h:mm:ss a', 'EN-US', tz);
          const popupContents = `
            Lat: ${element.lat}
            <br> Long: ${element.lng}
            <br> Date Reported: ${formattedDate}
            <br> <button class="delete">Blockage Cleared</button>
          `;
          let marker = L.marker([element.lat, element.lng], { icon: this.barrierIcon })
                        .bindPopup(popupContents, popupOptions)
          marker.addTo(this.myMap!);
          marker.on('popupopen', () => {
            this.myMap?.setView([element.lat, element.lng], this.myMap.getZoom(), {
              animate: true,
              duration: 1,
              easeLinearity: 0.25
            });

            [...this.elementRef.nativeElement.querySelectorAll('.delete')].pop()
              .addEventListener('click', () => {
                this.removeBlockage(element.id);
                this.myMap?.closePopup();
              });
          });
          this.blockagesMarksMap.set(element.id, marker);
        });

        // reset array
        this.blockagesNearby = [];
      }
    );
  }

  // remove all the blockage markers
  clearBlockageMarkers() {
    this.blockagesMarksMap.forEach((value: L.Marker, key: number) => {
      this.myMap?.removeLayer(value);
    });
    this.blockagesMarksMap.clear();
  }

  // send a blockage report
  reportBlockage() {
    var date = new Date();

    let postData = {
      lat: this.focusLocationLat,
      lng: this.focusLocationLng,
    }

    // post blockage to api
    this.blockageService.postBlockage(postData).subscribe( (res) => {
      // format date
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      const formattedDate = formatDate(date, 'MMM d, y, h:mm:ss a', 'EN-US', tz);

      // remove the mark so we can turn it to a blockage icon
      this.myMap?.removeLayer(this.focusLocationMark!);
      this.focusLocationMark = undefined;

      // set marker of the new blockage
      const popupContents = `
        Lat: ${res.lat}
        <br> Long: ${res.lng}
        <br> Date Reported: ${formattedDate}
        <br> <button class="delete">Blockage Cleared</button>
      `;

      let marker = L.marker([res.lat, res.lng], { icon: this.barrierIcon })
                    .bindPopup(popupContents, { className: "blockage-popup" })
      marker.addTo(this.myMap!);

      marker.on('popupopen', () => {
        this.myMap?.setView([res.lat, res.lng], this.myMap.getZoom(), {
          animate: true,
          duration: 1,
          easeLinearity: 0.25
        });

        [...this.elementRef.nativeElement.querySelectorAll('.delete')].pop()
          .addEventListener('click', () => {
            this.removeBlockage(res.id);
            this.myMap?.closePopup();
          });
      });

      this.blockagesMarksMap.set(res.id, marker);

      this.presentToast('Blockage report was successfully sent.', 'success')
    });
  }

  // called when pressing the button to remove blockage
  removeBlockage(id: number) {
    this.blockageService.deleteBlockage(id).subscribe( (res) => {
      let marker = this.blockagesMarksMap.get(id);
      this.myMap?.removeLayer(marker!);

      this.blockagesMarksMap.delete(id);
      this.presentToast('Successfully removed the blockage.', 'success')
    });
  }

  // run the simulation
  simulationRes: any = {};
  polylines: any[] = [];
  async runSimulation() {
    this.clearMapLines();

    // calculate viewport width/height -- bounds are square so we will get the larger value of the two
    var bounds = this.myMap?.getBounds();
    var width = this.myMap!.distance(bounds!.getNorthWest(), bounds!.getNorthEast());
    var height = this.myMap!.distance(bounds!.getNorthWest(), bounds!.getSouthWest());
    var distanceVal = Math.min(Math.max(width, height), 1000);  // limiting to 1000 meters because of performance issues

    const loading = await this.loadingCtrl.create({
      message: 'Calculating paths...',
    });
    loading.present();

    this.simulationService.getSimulation(this.myMap!.getCenter(), distanceVal).subscribe( (res) => {
      // show a loading screen
      this.simulationRes = {
        routes: JSON.parse(res.data.routes),
      }

      this.simulationRes.routes.features.forEach( (elem: any) => {
        var pl = L.polyline(
          L.GeoJSON.coordsToLatLngs(elem.geometry.coordinates, 0), {
            color: 'red'
          }).addTo(this.myMap!);
        this.polylines.push(pl);
      });

      this.presentToast('All pairs shortest paths displayed.', 'success')
      loading.dismiss();
    });
  }

  // run routing tool
  routesRes: any = {};
  srcMrker: any;
  dstMrker: any;
  async displayShortestPaths() {
    if (this.focusLocationLat == undefined || this.focusLocationLng == undefined) {
      this.presentToast('No destination selected.', 'danger')
      return;
    }

    this.clearMapLines();

    const loading = await this.loadingCtrl.create({
      message: 'Loading 5 shortest paths...',
    });
    loading.present();

    const sourceLatLng = L.latLng(this.initLat, this.initLng)
    const destinationLatLng = L.latLng(this.focusLocationLat, this.focusLocationLng)
    this.routesService.getRoutes(sourceLatLng, destinationLatLng).subscribe( (res) => {
      // show a loading screen
      this.routesRes = {
        routes: res.data,
      }
 
      // let colorList = ['#ff0000', '#4d4d4d', '#666666', '#808080', '#999999']
      let colorList = ['#999999', '#808080', '#666666', '#4d4d4d', '#ff0000']

      this.routesRes.routes.reverse().forEach( (elem: any, idx: number) => {
        var route = JSON.parse(elem)
        console.log(route)
        route.features.forEach( (e: any) => {
          var pl = L.polyline(
            L.GeoJSON.coordsToLatLngs(e.geometry.coordinates, 0), {
              color: colorList[idx]
            }).addTo(this.myMap!);
          this.polylines.push(pl);
        });
      });

      this.srcMrker = L.marker(sourceLatLng, { icon: this.locationIcon }).addTo(this.myMap!);
      this.srcMrker._icon.classList.add('routing-source');
      this.dstMrker = L.marker(sourceLatLng, { icon: this.locationIcon }).addTo(this.myMap!);
      this.dstMrker._icon.classList.add('routing-destination');

      this.presentToast('Top 5 shortest paths displayed.', 'success')
      loading.dismiss();
    });
  }

  clearMapLines() {
      if (this.srcMrker) this.myMap?.removeLayer(this.srcMrker);
      if (this.dstMrker) this.myMap?.removeLayer(this.dstMrker);

      this.polylines.forEach( (polyline: any) => {
        this.myMap?.removeLayer(polyline);
      })
      this.polylines = [];
  }


  async presentToast(message: string, color: string) {
    const toast = await this.toastController.create({
      message: message,
      duration: 2000,
      position: 'top',
      color: color,
      cssClass: 'toast-notification',
    });

    await toast.present();
  }

}
