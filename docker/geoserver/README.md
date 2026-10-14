# MBStyle extension

The GeoServer service mounts the three JARs in `plugins/mbstyle-2.28.5`
read-only into its `WEB-INF/lib` directory. Keep this directory with the
Compose project when moving or rebuilding the deployment. The original
plugin license and notices are included alongside the JARs.

Apply the configuration without upgrading the base image:

```sh
docker compose up -d --no-deps --pull never geoserver
```

Validated against the locally installed `geonode/geoserver:2.28.x-latest`
image containing GeoServer 2.28-SNAPSHOT and GeoTools 34-SNAPSHOT:
the module manifest lists MBStyle, the REST API accepts
`application/vnd.geoserver.mbstyle+json`, and WMS renders a polygon fill
using that style. The temporary validation style was removed afterward.
This verifies basic MBStyle rendering, not every style expression or source.

The base image tag is mutable. Recheck plugin compatibility before pulling
a newer image; the supplied extension targets GeoServer 2.28.5 / GeoTools 34.5.
To uninstall, remove the three MBStyle JAR volume entries from the GeoServer
service and recreate that service. Existing GeoServer data volumes are retained.
