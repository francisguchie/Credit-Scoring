/** Angular Imports */
import { Component, OnInit } from "@angular/core";
import { ScoreCardService } from "./scorecard.service";
import { Router, ActivatedRoute } from "@angular/router";
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import {MatSnackBar} from '@angular/material/snack-bar';

/**
 * Create Scorecard Component
 */
@Component({
  selector: "mifosx-scorecard",
  templateUrl: "./scorecard.component.html",
  styleUrls: ["./scorecard.component.scss"],
})

export class ScorecardComponent implements OnInit {

/**
 * Variable Declaration
 */

  model = ["Criteria", "Statistical", "Machine Learning"];
  displayedColumns: string[] = ["Category", "Feature", "Score", "Color"];
  public dataSource = [];
  columnsToDisplay: string[] = this.displayedColumns.slice();
  totalScore = 0;
  modelType: string[] = [];
  pred = "N/A";
  acc = "N/A";
  stat_pred = "N/A";
  stat_acc = "N/A";
  isRegSelected = false;
  stat_var_pred = "N/A";
  stat_var_risk = "N/A";
  isVarSelected = false;
  stat_wl_good = "N/A";
  stat_wl_bad = "N/A";
  stat_pred_wl_good = "N/A";
  stat_pred_wl_bad = "N/A";
  isMVSelected = false;
  criteria = false;
  ml = false;
  statistical = false;
  count_red = 0;
  count_green = 0;
  count_amber = 0;
  lin_reg = false;
  poly_reg = false;
  manova = false;
  stat_model = "";

  public scorecardObj = {
    age: [],
    ageweitage: 0,
    gender: [],
    genderweightage: 0,
  };
  errorFlag = false;
  colorgreen = false;
  scoregreen = '';
  coloramber = false;
  scoreamber = '';
  colorred = false;
  scorered = '';
  loanId = "";
  file = "";
  loanValues = [];
  res = [];

  constructor(private _scoreCardService: ScoreCardService, private router: Router, private route: ActivatedRoute, private _snackBar: MatSnackBar) {}
  ngOnInit() {
    this.getLoans();
  }

  /**
   * Helper Functions
   */

  public openSnackBar(message: string) {
    console.log(this);
    this._snackBar.open(message, "Close", {
      duration: 4000,
    });
  }

  public getLoans() {
    const successcallback = (data) => {
      for (let loan of data["pageItems"]) {
        let det = {
          id: loan["id"],
          clientId: loan["clientId"],
        };
        this.loanValues.push(det);
      }
    };
    this._scoreCardService.getLoan(successcallback);
  }

  public fileUpload() {
    console.log(this.file);
    const errorCallBack = (data) => {
      this.openSnackBar("Problem Uploading File, Please Check Link");
    }
    const uploadsuccesscallback = (data) => {
      console.log(data);
    }
    this._scoreCardService.uploadCSV(uploadsuccesscallback, this.file, errorCallBack);
  }


  public updateColor(color: string){
    if(color == 'green'){
      this.count_green = this.count_green + 1;
    }
    if(color == 'amber'){
      this.count_amber = this.count_amber + 1;
    }
    if(color == 'red'){
      this.count_red = this.count_red + 1;
    }
    if(this.count_green >= this.count_amber){
      this.colorgreen = false;
      this.coloramber = true;
      this.colorred = false;
    }
    if(this.count_green > this.count_amber){
      this.colorgreen = true;
      this.coloramber = false;
      this.colorred = false;
    }
    if(this.count_green + this.count_amber >= this.count_red){
      this.colorgreen = false;
      this.coloramber = true;
      this.colorred = false;
    }
    if(this.count_red >= this.count_amber && this.count_red >= this.count_green){
      this.colorgreen = false;
      this.coloramber = false;
      this.colorred = true;
    }
    console.log("Green Count");
    console.log(this.count_green);
  }

  public getStatisticalScoring(){
    const errorCallBack = (data) => {
      this.openSnackBar("Problem Calculating Statistical Score, Please check loan ID");
    }
    const statsuccesscallback = (data) => {
      console.log(data);
      if(data['scorecard']['method'] == "LinReg" || data['scorecard']['method'] == "PolyReg"){
        this.isRegSelected = true;
        this.isVarSelected = false;
        this.isMVSelected = false;
        this.stat_acc = data['scorecard']['prediction'];
        this.stat_pred = data['scorecard']['color'];
      }

      if(data['scorecard']['method'] == "VaR"){
        this.isRegSelected = false;
        this.isVarSelected = true;
        this.isMVSelected = false;
        this.stat_var_risk = data['scorecard']['Risk'];
        this.stat_var_pred = data['scorecard']['color'];
      }

      if(data['scorecard']['method'] == "MANOVA"){
        this.isRegSelected = false;
        this.isVarSelected = false;
        this.isMVSelected = true;
        this.stat_wl_good = data['scorecard']['WL_good'];
        this.stat_wl_bad = data['scorecard']['WL_bad'];
        this.stat_pred_wl_good = data['scorecard']['WL_test_good'];
        this.stat_pred_wl_bad = data['scorecard']['WL_test_bad'];
      }
    }
    this._scoreCardService.getStatScore(statsuccesscallback, this.loanId, this.stat_model, errorCallBack);
  }

  public getMLScoring(){
    const errorCallBack = (data) => {
      this.openSnackBar("Problem Calculating ML Score, Please check loan ID");
    }
    const mlsuccesscallback = (data) => {
      console.log(data);
      console.log(data['scorecard']["result"]);
      console.log(data['scorecard']["accuracy"])
      this.pred = data['scorecard']["result"];
      this.acc = data['scorecard']["accuracy"];
      this.acc = Number(this.acc).toFixed(2);
    }
    this._scoreCardService.getMLScore(mlsuccesscallback, this.loanId, errorCallBack);
  }

  public getRBScoring(){
    const errorCallBack = (data) => {
      this.openSnackBar("Problem Calculating RB Score, Please check loan ID");
    }
    console.log("RB");
    const rbsuccesscallback = (data) => {
      this.res.push({
        Category: data['scorecard']['category'],
        Feature: data['scorecard']['feature'],
        Score: data['scorecard']['score'],
        Color: data['scorecard']['color']
        });
      console.log(data);
    }
    this._scoreCardService.getRBScore(rbsuccesscallback, this.loanId, errorCallBack);
  }


/** 
 * Compile all the scores
 */

  public getClientDetails() {
    console.log(this.ml);
    console.log(this.statistical);
    console.log(this.criteria);
    if(this.statistical){
      console.log(this.stat_model);
      this.getStatisticalScoring();
    }
    if(this.ml){
      this.getMLScoring();
    }
    if(this.criteria){
      this.getRBScoring();
      this.errorFlag = false;
      this.colorgreen = false;
      this.coloramber = false;
      this.colorred = false;
      this.colorgreen = true;
      if (!this.loanId) {
        this.errorFlag = true;
      } else {
        let clientId = null;

        for (let loan of this.loanValues) {
          if (loan.id === +this.loanId) {
            clientId = loan.clientId;
            break;
          }
        }
        if (clientId) {
          const successcallback = (data) => {
            let dob = data["dateOfBirth"];
            let gender = data["gender"];

            console.log(dob);
            console.log("data : " + data.toString());
            let age = 0;
            let gen = "";
            if (dob) {
              age = new Date().getFullYear() - dob[0];
            }
            if (gender) {
              gen = gender["name"].toUpperCase();
            }
            console.log("GENDER", gen)
            const successcallbackGen = (datagen) => {
              console.log(datagen["genderScore"])
              this.totalScore = Number(datagen["ageScore"]) + Number(datagen["genderScore"]);
              this.res.push({
                Category: "Individual",
                Feature: " Age",
                Score: datagen["ageScore"],
                Color: datagen["ageColor"]
              });
              this.updateColor(datagen["ageColor"]);

              this.res.push({
                Category: "Individual",
                Feature: " Gender",
                Score: datagen["genderScore"],
                Color: datagen["genderColor"]
              });
              this.updateColor(datagen["genderColor"]);
            };
            this._scoreCardService.getAllScore(successcallbackGen, age, gen);
          };
          this._scoreCardService.getClientDetails(successcallback, clientId, this.openSnackBar);
        }
      }
      const errorCallBack = (data) => {
        this.openSnackBar(data);
      }
      let xmlsuccesscallback = (valueData) => {
        //data = JSON.parse(valueData)
        console.log(valueData['scorecard']['color'][0]);
        var count = 0;
        for(var i = 0; i < valueData['scorecard']['color'].length ; i++){
          count = count + Number(valueData['scorecard']['score'][i])
          this.res.push({
          Category: valueData['scorecard']['category'][i],
          Feature: valueData['scorecard']['feature'][i],
          Score: valueData['scorecard']['score'][i],
          Color: valueData['scorecard']['color'][i]
          });
          this.updateColor(valueData['scorecard']['color'][i]);
        }
        this.totalScore = this.totalScore + count;
      }
      
      let jsonsuccesscallback = (valueData) => {
        //data = JSON.parse(valueData)
        console.log(valueData['scorecard']['color'][0]);
        var count = 0;
        for(var i = 0; i < valueData['scorecard']['color'].length ; i++){
          count = count + Number(valueData['scorecard']['score'][i])
          this.res.push({
          Category: valueData['scorecard']['category'][i],
          Feature: valueData['scorecard']['feature'][i],
          Score: valueData['scorecard']['score'][i],
          Color: valueData['scorecard']['color'][i]
          });
          this.updateColor(valueData['scorecard']['color'][i]);
        }

        this.dataSource = this.res;
        this.totalScore = this.totalScore + count;
      }
      this._scoreCardService.getXmlScore(xmlsuccesscallback, this.loanId, errorCallBack);
      this._scoreCardService.getJsonScore(jsonsuccesscallback, this.loanId, errorCallBack);
    }
  }
}

export interface PeriodicElement {
  Category: string;
  Feature: string;
  Score: string;
  Color: string;
}
