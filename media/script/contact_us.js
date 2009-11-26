jQuery(function() {
  jQuery("#contact_us").qtip({
    position: {
      target: 'mouse',
      corner: {
        target: "bottomRight",
        tooltip: "bottomMidlle"
      }
    },
    style: {
      width: 350,
      padding: 5,
      color: 'black',
      textAlign: 'center',
      border: {
        radius: 5
      },
      name: 'light'
    }
  });
});

