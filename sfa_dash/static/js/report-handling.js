// on page load, insert an object pair
$(document).ready(function() {
  if ($('.object-pair-list')[0]){
      function registerAutocompleteSuggestionListeners(index){
        /* create an autocomplete to allow selection of the observation and forecast
         * the forecast autocomplete should be dependant on the site of the selected observation.
         */
      }

      function newPair(){
        /* Create a new observation, forecast input pair at the current index */
        var new_object_pair = $(`<li class="object-pair object-pair-${pair_index}">
                    <div class="form-element">
                      <label>Observation</label><br>
                      <div class="input-wrapper">
                        <input type="text" class="form-control  observation-field" name="observation-${pair_index}" value="">
                      </div>
                      <a data-toggle="collapse" data-target=".observation-${pair_index}-help-text" role="button" href="" class="help-button">?</a>
                      <span class="observation-${pair_index}-help-text form-text text-muted help-text collapse" aria-hidden="">Observation to compare Forecast against.</span>
                    </div>
                    <div class="form-element">
                      <label>Forecast</label><br>
                      <div class="input-wrapper">
                        <input type="text" class="form-control  forecast-field" name="forecast-${pair_index}" value="">
                      </div>
                      <a data-toggle="collapse" data-target=".forecast-${pair_index}-help-text" role="button" href="" class="help-button">?</a>
                      <span class="forecast-${pair_index}-help-text form-text text-muted help-text collapse" aria-hidden="">Forecast to compare.</span>
                    </div>
                 <a role="button" class="object-pair-delete-button">x</a>
                 </li>`);
          var remove_button = new_object_pair.find(".object-pair-delete-button");
          remove_button.click(function(){new_object_pair.remove();});
          return new_object_pair;
      }
      form = $('#report-form');
      pair_container = $('.object-pair-list');
      pair_index = 0;
      pair_container.append(newPair());
      pair_index++;
      $('#add-object-pair').click(function(){pair_container.append(newPair());pair_index++;});
  }
});

// List observation options when input has focus.
// Autocomplete or select list?


// Limit forecast options to forecasts at the same site
//

// on submit, collect and create 
