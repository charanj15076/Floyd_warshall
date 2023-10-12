import { TestBed } from '@angular/core/testing';

import { BlockageService } from './blockage.service';

describe('BlockageService', () => {
  let service: BlockageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BlockageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
