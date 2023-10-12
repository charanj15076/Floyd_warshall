import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonModal, IonicModule, SearchbarCustomEvent } from '@ionic/angular';

import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  ViewChild,
} from '@angular/core';

import OpenStreetMapProvider from 'leaflet-geosearch/lib/providers/openStreetMapProvider';

@Component({
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
  selector: 'app-geo-nav',
  templateUrl: './geo-nav.component.html',
  styleUrls: ['./geo-nav.component.scss'],
})


// this component controls the navigation/route planning functionality
export class GeoNavComponent  implements OnChanges {
  @Input() title = 'Search';
  @Input() trigger = 'trigger-element'
  @Output() selectedChanged: EventEmitter<any> = new EventEmitter();
  @ViewChild(IonModal) modal: IonModal | undefined;

  provider = new OpenStreetMapProvider({
    params: {
      countrycodes: 'us', // limit search results to the US
    },
  });
  results: any[] = [];

  selected: any;

  constructor() { }

  ngOnChanges() { }

  // click handler
  itemSelected(item: object) {
    this.selected = item;
    this.selectedChanged.emit(this.selected);

    // close modal and clear results
    this.modal!.dismiss();
    this.results = [];
  }

  // search feature - populates the list of matches
  async search(event: SearchbarCustomEvent) {
    const searchTerm = event?.detail?.value?.toLowerCase();
    this.results = await this.provider.search({ query: searchTerm! });
  }
}
