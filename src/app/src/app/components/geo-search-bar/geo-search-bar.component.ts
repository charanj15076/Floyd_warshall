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
  selector: 'app-geo-search-bar',
  templateUrl: './geo-search-bar.component.html',
  styleUrls: ['./geo-search-bar.component.scss'],
})

// this component controls the search functionality
export class GeoSearchBarComponent  implements OnChanges {
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
  showNoResults: boolean = false;

  selected: any;

  constructor() { }

  ngOnChanges() { }

  // click handler
  itemSelected(item: object) {
    this.showNoResults = false;
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
    this.showNoResults = true;
  }
}
