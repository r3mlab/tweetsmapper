function(cluster) {
    return new L.divIcon({
        html: '<div><span>' + cluster.getChildCount() + '</span></div>',
        className: 'marker-cluster marker-cluster-blue',
        iconSize: new L.Point(40, 40)
    });
}
