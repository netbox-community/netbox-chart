{{/* vim: set filetype=mustache: */}}

{{/*
Return the proper image name
*/}}
{{- define "netbox.image" -}}
{{- include "common.images.image" (dict "imageRoot" .Values.image "global" .Values.global "chart" .Chart) -}}
{{- end -}}

{{/*
Return the proper image name (for the init container image)
*/}}
{{- define "netbox.init.image" -}}
{{- include "common.images.image" (dict "imageRoot" .Values.init.image "global" .Values.global) -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "netbox.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "common.names.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Name of the Secret that contains the PostgreSQL password
*/}}
{{- define "netbox.postgresql.secret" -}}
  {{- if .Values.postgresql.enabled }}
    {{- include "postgresql.v1.secretName" .Subcharts.postgresql -}}
  {{- else }}
    {{- include "common.secrets.name" (dict "existingSecret" .Values.externalDatabase.existingSecretName "defaultNameSuffix" "postgresql" "context" $) }}
  {{- end }}
{{- end }}

{{/*
Name of the key in Secret that contains the PostgreSQL password
*/}}
{{- define "netbox.postgresql.secretKey" -}}
  {{- if .Values.postgresql.enabled -}}
    {{- include "postgresql.v1.userPasswordKey" .Subcharts.postgresql -}}
  {{- else if .Values.externalDatabase.existingSecretName -}}
    {{- .Values.externalDatabase.existingSecretKey -}}
  {{- else -}}
    db_password
  {{- end -}}
{{- end }}

{{/*
Name of the Secret that contains the Redis tasks password
*/}}
{{- define "netbox.tasksRedis.secret" -}}
  {{- if .Values.redis.enabled }}
    {{- include "redis.secretName" .Subcharts.redis -}}
  {{- else }}
    {{- include "common.secrets.name" (dict "existingSecret" .Values.tasksRedis.existingSecretName "defaultNameSuffix" "redis" "context" $) }}
  {{- end }}
{{- end }}

{{/*
Name of the key in Secret that contains the Redis tasks password
*/}}
{{- define "netbox.tasksRedis.secretKey" -}}
  {{- if .Values.redis.enabled -}}
    {{- include "redis.secretPasswordKey" .Subcharts.redis -}}
  {{- else if .Values.tasksRedis.existingSecretName -}}
    {{ .Values.tasksRedis.existingSecretKey }}
  {{- else -}}
    redis_tasks_password
  {{- end -}}
{{- end }}

{{/*
Name of the Secret that contains the Redis cache password
*/}}
{{- define "netbox.cachingRedis.secret" -}}
  {{- if .Values.redis.enabled }}
    {{- include "redis.secretName" .Subcharts.redis -}}
  {{- else }}
    {{- include "common.secrets.name" (dict "existingSecret" .Values.cachingRedis.existingSecretName "defaultNameSuffix" "redis" "context" $) }}
  {{- end }}
{{- end }}

{{/*
Name of the key in Secret that contains the Redis cache password
*/}}
{{- define "netbox.cachingRedis.secretKey" -}}
  {{- if .Values.redis.enabled -}}
    {{- include "redis.secretPasswordKey" .Subcharts.redis -}}
  {{- else if .Values.cachingRedis.existingSecretName -}}
    {{ .Values.cachingRedis.existingSecretKey }}
  {{- else -}}
    redis_cache_password
  {{- end -}}
{{- end }}

{{/*
Volumes that need to be mounted for .Values.extraConfig entries
*/}}
{{- define "netbox.extraConfig.volumes" -}}
{{- range $index, $config := .Values.extraConfig -}}
- name: extra-config-{{ $index }}
  {{- if $config.values }}
  configMap:
    name: {{ include "common.names.fullname" $ }}
    items:
    - key: extra-{{ $index }}.yaml
      path: extra-{{ $index }}.yaml
  {{- else if $config.configMap }}
  configMap:
    {{- toYaml $config.configMap | nindent 4 }}
  {{- else if $config.secret }}
  secret:
    {{- toYaml $config.secret | nindent 4 }}
  {{- end }}
{{ end -}}
{{- end }}

{{/*
Volume mounts for .Values.extraConfig entries
*/}}
{{- define "netbox.extraConfig.volumeMounts" -}}
{{- range $index, $config := .Values.extraConfig -}}
- name: extra-config-{{ $index }}
  mountPath: /run/config/extra/{{ $index }}
  readOnly: true
{{ end -}}
{{- end }}

{{/*
Compile all warnings into a single message.
*/}}
{{- define "netbox.validateValues" -}}
{{- $messages := list -}}
{{- $messages := append $messages (include "netbox.validateValues.postgresql" .) -}}
{{- $messages := without $messages "" -}}
{{- $message := join "\n" $messages -}}
{{- if $message -}}
{{-   printf "\nVALUES VALIDATION:\n%s" $message | fail -}}
{{- end -}}
{{- end -}}

{{/*
Validate values of Netbox Chart - PostgreSQL
*/}}
{{- define "netbox.validateValues.postgresql" -}}
{{- if and (not .Values.postgresql.enabled) (or (empty .Values.externalDatabase.host) (empty .Values.externalDatabase.port) (empty .Values.externalDatabase.database)) -}}
netbox: postgresql
    PostgreSQL installation has been disabled but without the required parameters
    to use an external database. To use an external database, please ensure you provide
    (at least) the following values:
        externalDatabase.host=DB_SERVER_HOST
        externalDatabase.database=DB_NAME
        externalDatabase.port=DB_SERVER_PORT
{{- end -}}
{{- end -}}
