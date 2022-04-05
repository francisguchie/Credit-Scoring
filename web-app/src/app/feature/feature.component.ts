/** Angular Imports */
import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FeatureService } from './feature.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import {MatSnackBar} from '@angular/material/snack-bar';

/**
 * Create Feature Screen Component
 */
@Component({
  selector: 'mifosx-feature',
  templateUrl: './feature.component.html',
  styleUrls: ['./feature.component.scss'],
})
export class FeatureComponent implements OnInit {
  valueData = ['Binary', 'Nominal', 'Interval', 'Ratio'];

  dataData = ['Numeric', 'Character', 'Date'];

  categoryData = ['Individual', 'Organisation', 'Country', 'CreditHistory', 'Loan'];
  errorMsg = '';
  public featureObject = {
    id: null,
    feature: '',
    valueType: '',
    dataType: '',
    category: '',
    status: '',
  };

  featureForm: FormGroup;

  constructor(private _featureService: FeatureService, private router: Router, private route: ActivatedRoute, private _snackBar: MatSnackBar) {}
  ngOnInit() {
    console.log("featuring")
    let id = null;

    let isCreateFeatureMode = this.router.url === "/feature";

    console.log(this.router.url, isCreateFeatureMode);



    this.featureForm = new FormGroup({
    'feature' : new FormControl({
    value: this.featureObject.feature,
    disabled: !isCreateFeatureMode
    }, [
    Validators.required,
    Validators.minLength(3),
    Validators.pattern("^[a-zA-Z0-9]*$")]),
    'valueType' : new FormControl(this.featureObject.valueType, []),
    'dataType' : new FormControl(this.featureObject.dataType, []),
    'category' : new FormControl(this.featureObject.category, []),
    'status' : new FormControl(this.featureObject.status, []),
    });

    this.route.params.subscribe((params) => {
    id = params['id'];
    });
    if (id) {
      this.getById(id);
    }
  }

  public openSnackBar(message: string) {
    console.log(this);
    this._snackBar.open(message, "Close", {
      duration: 4000,
    });
  }

  public submitFeature() {
    this.errorMsg = '';
    console.log(JSON.stringify(this.featureObject));
    console.log( this.featureObject.id &&
      this.featureObject.feature);

    if (
      this.featureObject.feature &&
      this.featureObject.valueType &&
      this.featureObject.dataType &&
      this.featureObject.category
    ) {
      const errorCallBack = (data) => {
        this.openSnackBar("Problem saving feature, Please try again !!");
      }
      const successcallback = (data) => {
        this.router.navigate(['configuration']);
      };
      this._featureService.saveFeature(this.featureObject, successcallback, errorCallBack);
    } else {
      this.errorMsg = 'All the fields are mandatory';
    }
  }

  public getById(id) {
    const errorCallBack = (data) => {
      this.openSnackBar("Problem getting feature details, Please check and retry !!");
    }
    const successcallback = (data) => {
      this.featureObject.category = data['category'];
      this.featureObject.dataType = data['data'];
      this.featureObject.feature = data['feature'];
      this.featureObject.valueType = data['value'];
      this.featureObject.id = data['id'];
      this.featureObject.status = data['status'];
    };
    this._featureService.getOneFeature(id, successcallback, errorCallBack);
  }
}
